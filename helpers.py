from datetime import date,timedelta,time
def daysOfweek(v=0):
    names=["Monday","Tuesday","Thursday","Wednesday","Friday","Saturday","Sunday"]
    today=date.today()
    weekday=today.weekday()
    firstday=today-timedelta(weekday)+timedelta(v)
    week=[firstday,]
    daynames=[names[firstday.weekday()],]
    for i in range (1,5):
        day=week[0]+timedelta(i)
        week.append(day)
        daynames.append(names[day.weekday()])
    return week,daynames
def ifWeekend():
    wd=date.today().weekday()
    if wd==5:
        return 3
    elif wd==6:
        return 4
    else:
        return 0
        
def toDate(datestr):
    return time.strptime(datestr,"%Y-%m-%d")
def getWeekNr(v=0,day=None):
    if day!=None:today=day
    else:
        today=date.today()+timedelta(v)
    return today.isocalendar()[1]