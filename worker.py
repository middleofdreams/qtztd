from db import DB
from PyQt4 import QtCore,QtGui
class Worker(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.db=DB('ztd.sqlite')
    def resort(self,db,widget):
		items=[]
		pos=[]
		for i in range(widget.count()):
			items.append(widget.item(i).itemid)
			pos.append(i)
		self.db.setPos(items,pos)
