import sqlite3
class DB(object):
    def __init__(self,dbpath):
        self.dbpath=dbpath
        self.conn=sqlite3.connect(dbpath)
    def getForDate(self,date):
        c=self.conn.cursor()
        t=(date,)
        c.execute('select * from tasks WHERE due_date=?',t)
        r=c.fetchall()
        c.close()
        return r
    def moveForDate(self,itemid,date):
        c=self.conn.cursor()
        t=(str(date),itemid)
        print t
        c.execute('Update Tasks Set due_date=? Where id=?',t)
        c.close()
        self.conn.commit()
    def setToDone(self,itemid,done):
        c=self.conn.cursor()
        t=(done,itemid)
        print t
        c.execute('Update Tasks Set done=? Where id=?',t)
        c.close()
        self.conn.commit()
    def editTask(self,itemid,name):
        c=self.conn.cursor()
        t=(str(name),itemid)
        print t
        c.execute('Update Tasks Set name=? Where id=?',t)
        c.close()
        self.conn.commit()
    def createTask(self,name,ddate):
        c=self.conn.cursor()
        t=(str(name),ddate)
        print t
        c.execute('Insert into Tasks (name,due_date) Values (?,?)',t)
        newid=c.lastrowid
        c.close()
        self.conn.commit()
        return newid