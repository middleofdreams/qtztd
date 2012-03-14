from PyQt4 import QtCore,QtGui
class Worker(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
    def resort(self,db,widget):
        for i in range(widget.count()):
            db.setPos(widget.item(i).itemid,i)