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
    def getForId(self,itemid):
        c=self.conn.cursor()
        t=(itemid,)
        c.execute('select * from tasks WHERE id=? ORDER BY pos',t)
        r=c.fetchall()
        c.close()
        return r
    def getForWeek(self,week,withoutdates=False):
        c=self.conn.cursor()
        t=(week,)
        if withoutdates:
            c.execute('select * from tasks WHERE due_date="thisweek" and due_week=? ORDER BY pos',t)
        else:
            c.execute('select * from tasks WHERE  due_week=? ORDER BY pos',t)
        r=c.fetchall()
        c.close()
        return r
    def moveForDate(self,itemid,date,due_week=None):
        c=self.conn.cursor()
        t=(str(date),due_week,itemid)
        c.execute('Update Tasks Set due_date=?, due_week=? Where id=?',t)
        c.close()
        self.conn.commit()
    def setToDone(self,itemid,done):
        c=self.conn.cursor()
        t=(done,itemid)
        c.execute('Update Tasks Set done=? Where id=?',t)
        c.close()
        self.conn.commit()
    def setPos(self,itemids,pos):
        c=self.conn.cursor()
        for i in pos:
            t=(i,itemids[i])
            c.execute('Update Tasks Set pos=? Where id=?',t)
        c.close()
        self.conn.commit()
    def editTask(self,itemid,name):
        c=self.conn.cursor()
        t=(unicode(name),itemid)
        c.execute('Update Tasks Set name=? Where id=?',t)
        c.close()
        self.conn.commit()
    def createTask(self,name,ddate=None,due_week=None):
        c=self.conn.cursor()
        if ddate=="thisweek":
            pos=len(self.getForWeek(due_week,True))
        else:
            pos=len(self.getForDate(ddate))
        t=(str(name),ddate,pos,due_week)
        c.execute('Insert into Tasks (name,due_date,pos,due_week) Values (?,?,?,?)',t)
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
    def checkIfNew(self,name):
        c=self.conn.cursor()
        t=(str(name),)
        c.execute('select * from tasks WHERE name=? COLLATE NOCASE',t)
        r=c.fetchall()
        c.close()
        if len(r)==0:
            return False
        else:
            return r[0]
    def getOutdated(self,currentdate,currentweek):
        c=self.conn.cursor()
        t=(False,currentdate,currentweek)
        c.execute('select * from tasks WHERE (done=? or done is NULL) and (due_date<? or (due_date="thisweek" and due_week<?)) ',t)
        r=c.fetchall()
        c.close()
        return r
    def deleteTask(self,itemid,):
        c=self.conn.cursor()
        t=(itemid,)
        c.execute("Delete from Tasks Where id=?",t)
        c.close()
        self.conn.commit()