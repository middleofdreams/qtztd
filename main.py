import sys
from PyQt4 import QtCore, QtGui
from ztd_ui import Ui_MainWindow
from helpers import *
from db import DB
from tasksmodel import *
from worker import Worker
class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None,dbpath='ztd.sqlite'):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.v=ifWeekend()
        self.db=DB(dbpath)
        self.prepareWidgets()
        self.fillWeek()
        self.ui.bottomPnl.hide()
        self.setWindowTitle("Qt ZTD - simple task management")
        self.options={'bottomPnlHidden':True}
    def prepareWidgets(self):
        self.ui.weekdays=[self.ui.weekday1,self.ui.weekday2,self.ui.weekday3,self.ui.weekday4,self.ui.weekday5,self.ui.inbox,self.ui.someday,self.ui.waiting,self.ui.thisweek]
        self.ui.taskslists=[]
        self.ui.lineeditlist=[]
        for i in range(0,9):
            taskwidget=TaskListWidget()
            lineedit=TaskLineEdit()
            self.ui.lineeditlist.append(lineedit)
            self.ui.taskslists.append(taskwidget)
            self.ui.weekdays[i].addWidget(lineedit)
            self.ui.weekdays[i].addWidget(taskwidget)
            self.connect(taskwidget,QtCore.SIGNAL("moveTask"),self.moveTask)
            self.connect(taskwidget,QtCore.SIGNAL("editTask"),self.editTask)
            self.connect(lineedit,QtCore.SIGNAL("createTask"),self.createNewTask)
            self.connect(taskwidget,QtCore.SIGNAL("taskDone"),self.taskDone)
            self.connect(taskwidget,QtCore.SIGNAL("sortTasks"),self.resortTask)

        self.ui.delete_label.setAcceptDrops(True)
        self.ui.delete_label.dropEvent=self.ldropEvent
        self.ui.delete_label.dragMoveEvent=self.ldragMoveEvent
        self.ui.delete_label.dragEnterEvent=self.ldragMoveEvent

    def fillWeek(self):    
        weekdays,names=daysOfweek(self.v)
        weekdays+=['inbox','someday','waiting',]
        for i in range(0,8):
            self.ui.taskslists[i].clear()
            self.ui.taskslists[i].setDate(weekdays[i])
            self.ui.lineeditlist[i].setDate(weekdays[i])
            if i<5:
                label=eval("self.ui.daylabel"+str(i+1))
                label.setText(str(names[i])+"<br/>"+str(weekdays[i]))
            tasks=self.db.getForDate(weekdays[i])
            for j in tasks:
                self.ui.taskslists[i].addItem(Task(j[1],j[0],j[6]))
        self.ui.taskslists[8].clear()
        self.ui.taskslists[8].setDate("thisweek")
        self.ui.taskslists[8].week=getWeekNr()
        self.ui.lineeditlist[8].setDate("thisweek")
        self.loadThisWeek()
    def loadThisWeek(self):
        self.ui.taskslists[8].clear()
        self.ui.taskslists[8].setDate("thisweek")
        self.ui.taskslists[8].week=getWeekNr()
        self.ui.lineeditlist[8].setDate("thisweek")
        tasks=self.db.getForWeek(getWeekNr())
        assigned=[]
        for j in tasks:
            n=Task(j[1],j[0],j[6])
            if j[2]!="thisweek":
                assigned.append(n)
                n.setFlags(QtCore.Qt.ItemFlags())
            else:
                self.ui.taskslists[8].addItem(n)
        for i in assigned:
            self.ui.taskslists[8].addItem(i)
    def moveTask(self,item,date,week):
        self.db.moveForDate(item.itemid, date, week)
        if date!="thisweek":
            self.loadThisWeek()

    def editTask(self,item):
        name=str(item.text()).strip()
        ifnew=self.db.checkIfNew(name)
        if not ifnew:
            self.db.editTask(item.itemid,name)
            self.loadThisWeek()
        else:
            old=self.db.getForId(item.itemid)
            item.setText(str(old[0][1]))
            msg=QtGui.QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText("Task already exists. It's marked due date: %s"%str(ifnew[2]))
            msg.show()
    def createNewTask(self,name,tdate,due_week):
        name=str(name).strip()
        ifnew=self.db.checkIfNew(name)
        if not ifnew:
            newid=self.db.createTask(name,tdate,due_week)
            for i in self.ui.taskslists:
                if i.date==tdate:
                    i.addItem(Task(name,newid))
            if due_week==getWeekNr():self.loadThisWeek()
        else:
            msg=QtGui.QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText("Task already exists. It's marked due date: %s"%str(ifnew[2]))
            msg.show()
    @QtCore.pyqtSlot()
    def on_next_clicked(self):
        self.v+=1
        self.fillWeek()
    @QtCore.pyqtSlot()
    def on_back_clicked(self):
        self.v-=1
        self.fillWeek()
    @QtCore.pyqtSlot()
    def on_next_week_clicked(self):
        self.v+=7
        self.fillWeek()
    @QtCore.pyqtSlot()
    def on_back_week_clicked(self):
        self.v-=7
        self.fillWeek()
    @QtCore.pyqtSlot()
    def on_bottomPanel_btn_clicked(self):
        if self.options['bottomPnlHidden']:
            self.options['bottomPnlHidden']=False
            self.ui.bottomPnl.show()
        else:
            self.options['bottomPnlHidden']=True
            self.ui.bottomPnl.hide()            
    def createTask(self,name):
        return Task(name)
    def taskDone(self,itemid,done):
        self.db.setToDone(itemid,done)
        self.loadThisWeek()
    def resortTask(self,widget):
        items=[]
        pos=[]
        disableds=0
        for i in range(widget.count()):
            if widget.item(i).flags()==QtCore.Qt.ItemFlags():
                disableds+=1
            else:
                items.append(widget.item(i).itemid)
            pos.append(i-disableds)
        self.worker=Worker(items,pos,self)
        self.connect(self.worker,QtCore.SIGNAL("finished"),self.loadThisWeek)

        self.worker.run()
    def ldropEvent(self,e):
        e.accept()
        r=e.source().row(e.source().currentItem())
        item=e.source().takeItem(r)
        self.db.deleteTask(item.itemid)
        del(item)
        self.loadThisWeek()
    def ldragMoveEvent(self,e):
        e.accept()
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if len(sys.argv)==2:
        myapp = MyForm(dbpath=sys.argv[1])
    else:
        myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
