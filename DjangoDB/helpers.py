import datetime
import io

import matplotlib.pyplot as plt
import math
def getCurrentDayMonthYear():
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    return day, month, year

