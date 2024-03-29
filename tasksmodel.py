from PyQt4 import QtCore,QtGui
from datetime import date
import sip
from helpers import getWeekNr
class TaskListWidget(QtGui.QListWidget):
    def __init__(self, parent=None, *args): 
        """ datain: a list where each item is a row
        """
        QtGui.QListWidget.__init__(self, parent, *args)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.showDropIndicator()
        self.setDropIndicatorShown(True)
        self.dropIndicatorPosition()
        self.connect(self, QtCore.SIGNAL("itemChanged(QListWidgetItem *)"), self.itemChanged)
 
        self.connect(self, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *,QListWidgetItem *)"), self.currentItemChanged)
 
        self.past=False
    def currentItemChanged(self,new,old):
        self.closePersistentEditor(old)
            
    def keyPressEvent(self,e):
        if e.key()==QtCore.Qt.Key_Escape:
            self.closePersistentEditor(self.currentItem())
    def mousePressEvent(self,mouseEvent):
        item=self.itemAt(mouseEvent.pos())
        if item!=None and item.flags()==QtCore.Qt.ItemFlags():
            self.clearSelection()
        else:
            QtGui.QListWidget.mousePressEvent(self,mouseEvent)
    def mouseDoubleClickEvent(self, mouseEvent):
        item= self.itemAt(mouseEvent.pos())
        if item:
            if item.flags()!=QtCore.Qt.ItemFlags():
                if QtCore.Qt.LeftButton == mouseEvent.button():
                    print self.date
                    if not self.past or item.done_status==None or item.done_status==False or self.date=="outdated":
                        print "dsasda"
                        item.done()
                        print item.itemid,item.done_status
                        self.emit(QtCore.SIGNAL("taskDone"),item.itemid,item.done_status)
    
                else: 
                    self.openPersistentEditor(item)
                    item.editable=True
            

    def setDate(self,tdate,week=None):
        self.current=False
        self.past=False
        self.setAcceptDrops(True)
        self.date=tdate
        self.week=week
        slist=['inbox','someday','thisweek','waiting','outdated']
        if not (tdate in slist):
            qpal=QtGui.QPalette()
            self.week=getWeekNr(day=tdate)
            if self.date==date.today():
                self.current=True
                qpal.setColor(QtGui.QPalette.Base,QtGui.QColor('#F5F3C4'))
                self.setPalette(qpal)
            elif self.date<date.today():
                #self.setAcceptDrops(False)
                self.past=True
                qpal.setColor(QtGui.QPalette.Base,QtGui.QColor('#C9C9C9'))
                self.setPalette(qpal)     
            else:
                self.setPalette(qpal) 

    def itemChanged(self,item, *args):
        if isinstance(item,Task):
            if item.editable:
                item.editable=False
                self.emit(QtCore.SIGNAL("editTask"),item)
            try:
                self.closePersistentEditor(item)
            except: pass
    def dragMoveEvent(self, event):
        if event.source().currentItem().done_status or not self.past:
            event.accept()
            QtGui.QListWidget.dragMoveEvent(self,event)
        else:
            event.ignore()
    def addItem(self,item):
        self.boldItem(item)
        QtGui.QListWidget.addItem(self,item)
    def insertItem(self,row,item):
        self.boldItem(item)
        QtGui.QListWidget.insertItem(self,row,item)       
    #testest
    def boldItem(self,item):
        if self.current:b=500
        else: b=50
        f=item.font()
        f.setWeight(b)
        item.setFont(f)
        
    def dropEvent(self, event):
        #self.setDisabled(True)
        olditem=event.source().currentItem()
        currentrow=event.source().row(olditem)
        item=event.source().takeItem(currentrow)
        if self.date!="thisweek" or self==event.source() or event.source().week!=getWeekNr():
            QtGui.QListWidget.dropEvent(self,event)
        newItem=self.findItems(olditem.text(),QtCore.Qt.MatchExactly)[0]
        row=self.row(newItem)
        
        o=self.takeItem(row)
        del(o)
        if event.source()!=self:
            self.insertItem(row,item)
            self.emit(QtCore.SIGNAL("moveTask"),item,self.date,self.week)

        else:
            del(olditem)
            self.insertItem(row,item)  
        event.accept()       
        #self.setEnabled(True)
        #self.emit(QtCore.SIGNAL("sortTasks"),event.source())

        self.emit(QtCore.SIGNAL("sortTasks"),self)
        if event.source().date=="outdated":self.emit(QtCore.SIGNAL("loadOutdated"),event.source())

class Task(QtGui.QListWidgetItem):
    def __init__(self,text,itemid,done=False,parent=None,*args):
        QtGui.QListWidgetItem.__init__(self, text,parent, *args)
        self.itemid=itemid
        self.done_status=done
        if done: self.done()
#       self.setData(3,itemid)
        self.editable=False
    def clone(self):
        c= Task(self.text(),self.itemid)
        c.done_status=self.done_status
        if c.done_status:
            c.done()
        return c
    def done(self):
        f=self.font()
        f.setStrikeOut(not f.strikeOut())
        self.setFont(f)
        self.done_status=f.strikeOut()

    
class TaskLineEdit(QtGui.QLineEdit):
    def __init__(self,date=None,parent=None,*args):
        QtGui.QLineEdit.__init__(self,parent, *args)
        self.connect(self, QtCore.SIGNAL("returnPressed()"), self.returnPressed) 
        self.setMaxLength(255)
    def setDate(self,ldate,week=None):
        self.date=ldate
        self.week=week
        slist=['inbox','someday','thisweek','waiting']
        if not (ldate in slist):
            self.week=getWeekNr(day=self.date)
            if self.date<date.today():
                self.setDisabled(True)
            else:
                self.setEnabled(True)
        elif self.date=="thisweek":
            self.week=getWeekNr()
        
    def returnPressed(self):
        if not unicode(self.text()).strip()=="":
            text=self.text()
            self.setText("")
            self.emit(QtCore.SIGNAL("createTask"),text,self.date,self.week)

        
