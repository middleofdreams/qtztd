from db import DB
from PyQt4 import QtCore,QtGui
class Worker(QtCore.QThread):
    def __init__(self, items,pos, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.db=parent.db
        self.pos=pos
        self.items=items
    def run(self):
        self.db.setPos(self.items,self.pos)
