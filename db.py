import sqlite3
class DB(object):
    def __init__(self,dbpath):
        self.dbpath=dbpath
        self.conn=sqlite3.connect(dbpath)
    def getForDate(self,date):
        c=self.conn.cursor()
        t=(date,)
        c.execute('select * from tasks WHERE due_date=? ORDER BY pos',t)
        r=c.fetchall()
        c.close()
        return r
    def moveForDate(self,itemid,date):
        c=self.conn.cursor()
        t=(str(date),itemid)
        c.execute('Update Tasks Set due_date=? Where id=?',t)
        c.close()
        self.conn.commit()
    def setToDone(self,itemid,done):
        c=self.conn.cursor()
        t=(done,itemid)
        c.execute('Update Tasks Set done=? Where id=?',t)
        c.close()
        self.conn.commit()
    def setPos(self,itemid,pos):
        c=self.conn.cursor()
        t=(pos,itemid)
        c.execute('Update Tasks Set pos=? Where id=?',t)
        c.close()
        self.conn.commit()
    def editTask(self,itemid,name):
        c=self.conn.cursor()
        t=(unicode(name),itemid)
        c.execute('Update Tasks Set name=? Where id=?',t)
        c.close()
        self.conn.commit()
    def createTask(self,name,ddate=None):
        self
        c=self.conn.cursor()
        pos=len(self.getForDate(ddate))
        t=(str(name),ddate,pos)
        c.execute('Insert into Tasks (name,due_date,pos) Values (?,?,?)',t)
        newid=c.lastrowid
        c.close()
        self.conn.commit()
        return newid
    def setAttr(self,itemid,attrname,attrvalue):
        c=self.conn.cursor()
        t=(attrname,attrvalue,itemid)
        c.execute("Update Tasks Set ?=? Where id=?",t)
        c.close()
        self.conn.commit()
