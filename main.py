import sys
from PyQt4 import QtCore, QtGui
from ztd_ui import Ui_MainWindow
from helpers import *
from db import DB
from tasksmodel import *
class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.v=0
        self.db=DB('ztd.sqlite')
        self.prepareWidgets()
        self.fillWeek()
    def prepareWidgets(self):
        self.ui.weekdays=[self.ui.weekday1,self.ui.weekday2,self.ui.weekday3,self.ui.weekday4,self.ui.weekday5]
        self.ui.taskslists=[]
        self.ui.lineeditlist=[]
        for i in range(0,5):
            taskwidget=TaskListWidget()
            lineedit=TaskLineEdit()
            self.ui.lineeditlist.append(lineedit)
            self.ui.taskslists.append(taskwidget)
            self.ui.weekdays[i].addWidget(lineedit)
            self.ui.weekdays[i].addWidget(taskwidget)
            self.connect(taskwidget,QtCore.SIGNAL("moveTask"),self.moveTask)
            self.connect(taskwidget,QtCore.SIGNAL("editTask"),self.editTask)
            self.connect(lineedit,QtCore.SIGNAL("createTask"),self.createNewTask)
            self.connect(taskwidget,QtCore.SIGNAL("taskDone"),self.db.setToDone)


    def fillWeek(self):    
        weekdays,names=daysOfweek(self.v)
        for i in range(0,5):
            label=eval("self.ui.daylabel"+str(i+1))
            label.setText(str(names[i])+"<br/>"+str(weekdays[i]))
            tasks=self.db.getForDate(weekdays[i])
            self.ui.taskslists[i].clear()
            self.ui.taskslists[i].setDate(weekdays[i])
            self.ui.lineeditlist[i].setDate(weekdays[i])
            for j in tasks:
                self.ui.taskslists[i].addItem(Task(j[1],j[0],j[9]))
           
    
    def moveTask(self,itemid,date):
        self.db.moveForDate(itemid, date)
    def editTask(self,itemid,name):
        self.db.editTask(itemid,name)
    def createNewTask(self,name,tdate):
        newid=self.db.createTask(name,tdate)
        for i in self.ui.taskslists:
            if i.date==tdate:
                i.addItem(Task(name,newid))
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
    def createTask(self,name):
        return Task(name)
   


 
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())