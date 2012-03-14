from datetime import date,timedelta
def daysOfweek(v=0):
    print v
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
