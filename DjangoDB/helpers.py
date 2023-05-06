import datetime
import io
import matplotlib.pyplot as plt
import math

def getCurrentDayMonthYear():
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    return day, month, year


def deleteAllParenthese(country):
    if '(' in str(country):
         country = str(country).replace("(", "").replace(")", "")
    return country


def switchForCase(case):
    if case == "confirmed":
        return "confirmed", "Confirmed"
    elif case == "death":
        return "deaths", "Deaths"
    elif case == "recovered":
        return 'recovered', "Recovered"

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

def create_two_countries_plot(first_country, second_country, case, y_label, x_label, first_country_df, second_country_df):
    fig, ax = plt.subplots()
    dates = first_country_df[x_label]

    ax.plot(first_country_df[x_label], first_country_df[y_label], label=first_country)
    ax.plot(second_country_df[x_label], second_country_df[y_label], label=second_country)
    middle = math.ceil(len(dates) / 2)

    plt.xticks([dates[0], dates[middle], dates[len(dates) - 1]], visible=True)
    ax.set_title(f"COVID-19 {case} cases comprassion")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"{case} Cases")
    ax.legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    return buffer