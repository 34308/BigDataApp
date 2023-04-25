import datetime
import io
import matplotlib.pyplot as plt
import math

from DjangoDB.Tables import confirmedCasesForCountries, deathCasesForCountries, recoveredCasesForCountries


def getCurrentDayMonthYear():
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    return day, month, year


def switchForCase(case):
    if case == "confirmed":
        return "confirmed", "Confirmed", confirmedCasesForCountries
    elif case == "death":
        return "deaths", "Deaths", deathCasesForCountries
    elif case == "recovered":
        return 'recovered', "Recovered", recoveredCasesForCountries


def plotCreator(country, case, ylabel, xlabel, df):
    fig, ax = plt.subplots()
    dates = df[xlabel]

    ax.plot(df[xlabel], df[ylabel])
    middle = math.ceil(len(dates) / 2)

    plt.xticks([dates[0], dates[middle], dates[len(dates) - 1]], visible=True)
    ax.set_title(f"COVID-19 {case} Cases in " + country)
    ax.set_xlabel("Date")
    ax.set_ylabel(f"{case} Cases")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    return buffer
