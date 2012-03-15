from PyQt4 import QtCore,QtGui
from datetime import date
import sip
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
        
    def mouseDoubleClickEvent(self, mouseEvent):
        item= self.itemAt(mouseEvent.pos())
        if item:
            if QtCore.Qt.LeftButton == mouseEvent.button():
                if not self.past:
                    item.done()
                    self.emit(QtCore.SIGNAL("taskDone"),item.itemid,item.done_status)

            else: self.openPersistentEditor(item)
            

    def setDate(self,tdate):
        self.current=False
        self.setAcceptDrops(True)
        self.date=tdate
        qpal=QtGui.QPalette()
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
            self.emit(QtCore.SIGNAL("editTask"),item.itemid,item.text())
            self.closePersistentEditor(item)
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
        self.setDisabled(True)
        olditem=event.source().currentItem()
        currentrow=event.source().row(olditem)
        item=event.source().takeItem(currentrow)
        QtGui.QListWidget.dropEvent(self,event)
        newItem=self.findItems(olditem.text(),QtCore.Qt.MatchExactly)[0]
        row=self.row(newItem)
        o=self.takeItem(row)
        del(o)
        if event.source()!=self:
            self.insertItem(row,item)
            self.emit(QtCore.SIGNAL("moveTask"),item.itemid,self.date)
        else:
            del(olditem)
            self.insertItem(row,item)  
        event.accept()       
        self.setEnabled(True)
        self.emit(QtCore.SIGNAL("sortTasks"),self)
        #self.emit(QtCore.SIGNAL("sortTasks"),event.source())
class Task(QtGui.QListWidgetItem):
    def __init__(self,text,itemid,done=False,parent=None,*args):
        QtGui.QListWidgetItem.__init__(self, text,parent, *args)
        self.itemid=itemid
        self.done_status=done
        if done: self.done()
        self.setData(3,itemid)
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
        self.setMaxLength(30)
    def setDate(self,ldate):
        self.date=ldate
        if self.date<date.today():
            self.setDisabled(True)
        else:
            self.setEnabled(True)
    def returnPressed(self):
        if not unicode(self.text()).strip()=="":
            text=self.text()
            self.setText("")
            self.emit(QtCore.SIGNAL("createTask"),text,self.date)

        
