import math
from datetime import datetime

import requests
import urllib, json
from django.http import JsonResponse, HttpResponse
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import io
import base64
from django.http import JsonResponse
from DjangoDB.databaseConnector import updateOrCrateDataTable, updateOrCrateDataTableWithIdentifier,getDatabase
from DjangoDB.helpers import getCurrentDayMonthYear


def listOfCountriesWichWeHaveDataOn(request):
    response = requests.get("https://api.covid19api.com/summary")
    data = response.json()
    countries = [c['Country'] for c in data['Countries']]
    new_data = {"countries": countries}
    json_data = json.dumps(new_data)
    data_dict = json.loads(json_data)
    updateOrCrateDataTable('ListOfCountries',data_dict)

    return JsonResponse(data_dict, safe=False)


def counrtyWithMostDeaths(request):
    response = requests.get("https://api.covid19api.com/summary")
    data = response.json()
    countries=data["Countries"]
    df=pd.json_normalize(countries)
    sorted_df = df.sort_values('TotalDeaths', ascending=False)
    highest_deaths = sorted_df.head(1)
    result_dict = highest_deaths.to_dict(orient='records')[0]
    result_dict = {'Country': result_dict['Country'], 'death_Cases': result_dict['TotalDeaths']}
    result_json = json.dumps(result_dict)
    result_json = json.loads(result_json)

    updateOrCrateDataTable('CountryWithMostDeaths',result_json)
    return JsonResponse(result_json, safe=False)

def allRecoveredCasesForCountryTillNowPlot(request,country):
    day,month,year=getCurrentDayMonthYear()
    url=f'https://api.covid19api.com/country/'+country+'/status/recovered/live?from=2020-03-01T00:00:00Z&to='+str(year)+'-0'+str(month)+'-'+str(day)+'T00:00:00Z'
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)
    df = df.drop(["CountryCode", "Province", "City", "CityCode", "Lat", "Lon"], axis=1)
    json_str = df.to_json(orient="records")

    updateOrCrateDataTableWithIdentifier("RecoveredCasesForCountries",json.loads(json_str),country)
    fig, ax = plt.subplots()
    dates = df['Date']
    middle = math.ceil(len(dates) / 2)

    ax.plot(df["Date"], df["Cases"])
    my_xticks = ax.get_xticks()
    plt.xticks([my_xticks[0], my_xticks[middle], my_xticks[-1]], visible=True)
    ax.set_title("COVID-19 Recovered Cases in " + country)
    ax.set_xlabel("Date")
    ax.set_ylabel("Recovered Cases")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    return HttpResponse(buffer.getvalue(), content_type="image/png")

def allDeathCasesForCountryTillNowPlot(request,country):
    day,month,year=getCurrentDayMonthYear()
    url=f'https://api.covid19api.com/country/'+country+'/status/deaths/live?from=2020-03-01T00:00:00Z&to='+str(year)+'-0'+str(month)+'-'+str(day)+'T00:00:00Z'
    print(url)
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)
    df = df.drop(["CountryCode", "Province", "City", "CityCode", "Lat", "Lon"], axis=1)
    json_str = df.to_json(orient="records")

    updateOrCrateDataTableWithIdentifier("DeathCasesForCountries",json.loads(json_str),country)

    dates = df['Date']
    fig, ax = plt.subplots()

    ax.plot(dates, df["Cases"])
    my_xticks = ax.get_xticks()
    middle=math.ceil(len(dates)/2)

    plt.xticks([my_xticks[0], my_xticks[middle],my_xticks[-1]],visible=True)
    ax.set_title("COVID-19 Death Cases in " + country)
    ax.set_xlabel("Date")
    ax.set_ylabel("deaths Cases")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    return HttpResponse(buffer.getvalue(), content_type="image/png")
def allConfirmedCasesForCountryTillNowPlot(request, country):
    url = f'https://api.covid19api.com/total/dayone/country/{country}'
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)

    fig, ax = plt.subplots()
    dates = df['Date']
    middle = math.ceil(len(dates) / 2)
    ax.plot(dates, df["Confirmed"])
    my_xticks = ax.get_xticks()
    plt.xticks([my_xticks[0], my_xticks[middle], my_xticks[-1]], visible=True)

    ax.set_title("COVID-19 Confirmed Cases in " + country)
    ax.set_xlabel("Date")
    ax.set_ylabel("Confirmed Cases")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')

    plt.close(fig)

    return HttpResponse(buffer.getvalue(), content_type="image/png")

def updateAllData(request):

    return allDeathCasesForCountryTillNowPlot(request,"poland")