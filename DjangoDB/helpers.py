import datetime
def getCurrentDayMonthYear():
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    return day, month, year
