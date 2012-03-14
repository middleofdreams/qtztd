from PyQt4 import QtCore,QtGui
from datetime import date
class TaskListWidget(QtGui.QListWidget):
    def __init__(self, parent=None, *args): 
        """ datain: a list where each item is a row
        """
        QtGui.QListWidget.__init__(self, parent, *args)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.connect(self, QtCore.SIGNAL("itemChanged(QListWidgetItem *)"), self.itemChanged) 
        self.connect(self, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *,QListWidgetItem *)"), self.currentItemChanged) 
    
    def currentItemChanged(self,new,old):
        self.closePersistentEditor(old)
            
    def keyPressEvent(self,e):
        if e.key()==QtCore.Qt.Key_Escape:
            self.closePersistentEditor(self.currentItem())
        
    def mouseDoubleClickEvent(self, mouseEvent):
        item= self.itemAt(mouseEvent.pos())
        if item:
            if QtCore.Qt.LeftButton == mouseEvent.button():
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
            self.setAcceptDrops(False)
            qpal.setColor(QtGui.QPalette.Base,QtGui.QColor('#C9C9C9'))
            self.setPalette(qpal)     
        else:
            self.setPalette(qpal) 
    

    def itemChanged(self,item, *args):
        self.emit(QtCore.SIGNAL("editTask"),item.itemid,item.text())
        self.closePersistentEditor(item)
    def dragMoveEvent(self, event):
        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()
    def addItem(self,item):
        if self.current:
            f=item.font()
            f.setWeight(500)
            item.setFont(f)
        QtGui.QListWidget.addItem(self,item)
        
    #testest
    def dropEvent(self, event):
        #QtGui.QListWidget.dropEvent(self,event)
        item=event.source().currentItem().clone()
        self.addItem(item)
        print item.done_status
        if event.source()!=self:
            self.emit(QtCore.SIGNAL("moveTask"),item.itemid,self.date)
        event.accept()

class Task(QtGui.QListWidgetItem):
    def __init__(self,text,itemid,done=False,parent=None,*args):
        QtGui.QListWidgetItem.__init__(self, text,parent, *args)
        self.itemid=itemid
        self.done_status=done
        if done: self.done()
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

    def setDate(self,ldate):
        self.date=ldate
        if self.date<date.today():
            self.setDisabled(True)
        else:
            self.setEnabled(True)
    def returnPressed(self):
        text=self.text()
        self.setText("")
        self.emit(QtCore.SIGNAL("createTask"),text,self.date)

        