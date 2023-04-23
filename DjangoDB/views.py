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

from DjangoDB.Tables import listOfCountries, countryWithMostDeaths, recoveredCasesForCountries, deathCasesForCountries, \
    confirmedCasesForCountries, Cases, CaseTable
from DjangoDB.databaseConnector import updateOrCrateDataTable, updateOrCrateDataTableWithIdentifier, getDatabase, \
    GetDataTableWithIdentifier
from DjangoDB.helpers import getCurrentDayMonthYear, plotCreator, switchForCase


def listOfCountriesWichWeHaveDataOn(request):
    response = requests.get("https://api.covid19api.com/summary")
    data = response.json()
    countries = [c['Country'] for c in data['Countries']]
    new_data = {"countries": countries}
    json_data = json.dumps(new_data)
    data_dict = json.loads(json_data)
    updateOrCrateDataTableWithIdentifier(listOfCountries, data_dict,listOfCountries)

    return JsonResponse(data_dict, safe=False)


def counrtyWithMostDeaths(request):
    response = requests.get("https://api.covid19api.com/summary")
    data = response.json()
    countries = data["Countries"]
    df = pd.json_normalize(countries)
    sorted_df = df.sort_values('TotalDeaths', ascending=False)
    highest_deaths = sorted_df.head(1)
    result_dict = highest_deaths.to_dict(orient='records')[0]
    result_dict = {'Country': result_dict['Country'], 'death_Cases': result_dict['TotalDeaths']}
    result_json = json.dumps(result_dict)
    result_json = json.loads(result_json)

    updateOrCrateDataTableWithIdentifier(countryWithMostDeaths, result_json,countryWithMostDeaths)
    return JsonResponse(result_json, safe=False)


def CasesForCountryTillNowFromDatabase(request, case, country):
    url_part, status, table = switchForCase(case)
    dataTable = GetDataTableWithIdentifier(table, country)

    df = pd.json_normalize(dataTable["data"])
    buffer = plotCreator(country, status, "Cases", "Date", df)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def CasesForCountryTillNowFromNet(request, case, country):
    url_part, status, table = switchForCase(case)
    day, month, year = getCurrentDayMonthYear()
    url = f'https://api.covid19api.com/country/' + country + f'/status/{url_part}/live?from=2020-03-01T00:00:00Z&to=' + str(
        year) + '-0' + str(month) + '-' + str(day) + 'T00:00:00Z'
    print(url)
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)
    df = df.drop(["CountryCode", "Province", "City", "CityCode", "Lat", "Lon"], axis=1)
    json_str = df.to_json(orient="records")

    updateOrCrateDataTableWithIdentifier(table, json.loads(json_str), country)
    buffer = plotCreator(country, status, "Cases", "Date", df)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def getAllCasesForCountryToDatabase(request, country):
    cases = ["confirmed", "death", "recovered"]
    for case in cases:
        url_part, status, table = switchForCase(case)
        day, month, year = getCurrentDayMonthYear()
        url = f'https://api.covid19api.com/country/' + country + f'/status/{url_part}/live?from=2020-03-01T00:00:00Z&to=' + str(
            year) + '-0' + str(month) + '-' + str(day) + 'T00:00:00Z'
        print(url)
        response = requests.get(url)
        data = response.json()
        df = pd.json_normalize(data)
        df = df.drop(["CountryCode", "Province", "City", "CityCode", "Lat", "Lon"], axis=1)
        json_str = df.to_json(orient="records")

        updateOrCrateDataTableWithIdentifier(table, json.loads(json_str), country)
    result_json = {"data":[f"Confirmed, Deaths, Recovered cases for {country}, correctly saved to database"]}
    return JsonResponse(result_json, safe=False)

def getAllCasesForAllCountriesToDatabase(request):
    data=GetDataTableWithIdentifier(listOfCountries,listOfCountries)["data"]
    data_dict = json.loads(json.dumps(data))
    countries = data_dict['countries']
    #poki co nie uzywać skrashowałem api.covid ostatnio
    # for country in countries:
    #     cases = ["confirmed", "death", "recovered"]
    #     for case in cases:
    #         url_part, status, table = switchForCase(case)
    #         day, month, year = getCurrentDayMonthYear()
    #         url = f'https://api.covid19api.com/country/' + country + f'/status/{url_part}/live?from=2020-03-01T00:00:00Z&to=' + str(
    #             year) + '-0' + str(month) + '-' + str(day) + 'T00:00:00Z'
    #         print(url)
    #         response = requests.get(url)
    #         data = response.json()
    #         print(case,country)
    #         df = pd.json_normalize(data)
    #         columns_to_drop=["CountryCode", "Province", "City", "CityCode", "Lat", "Lon"]
    #         for col in columns_to_drop:
    #             if col in df.columns:
    #                 df = df.drop(col, axis=1)
    #         json_str = df.to_json(orient="records")
    #         updateOrCrateDataTableWithIdentifier(table, json.loads(json_str), country)
    result_json = {"data":[f"Confirmed, Deaths, Recovered cases for All countries, correctly saved to database"]}
    return JsonResponse(result_json, safe=False)