import math
from datetime import datetime

import requests
import urllib, json
from django.http import JsonResponse, HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pymongo import MongoClient
from bson import ObjectId

import io
import base64
import time
from django.http import JsonResponse

from DjangoDB.Tables import listOfCountries, countryWithMostDeaths, Cases, basic_date, casesForCountry, \
    countryWithLeastDeaths
from DjangoDB.databaseConnector import updateOrCrateDataTable, updateOrCrateDataTableWithIdentifier, getDatabase, \
    GetDataTableWithIdentifier, updateOrCrateDataTableWithIdentifierWithDb
from DjangoDB.helpers import getCurrentDayMonthYear, plotCreator, switchForCase, create_two_countries_plot, \
    piePlotCreator


def getListOfCountriesWichWeHaveDataOn(request):
    data = GetDataTableWithIdentifier(listOfCountries, listOfCountries)
    df = pd.json_normalize(data["data"])
    string_json = df.to_json(orient="records")
    proper_json = json.loads(string_json)

    return JsonResponse(proper_json , safe=False,content_type='application/json')


def getCountryWithMostDeathsData(request):
    dataTable = GetDataTableWithIdentifier(countryWithMostDeaths, "CountryWithMostDeaths")
    df = pd.json_normalize(dataTable["data"])
    string_json = df.to_json(orient="records")
    string_json = '[' + string_json + ']'
    result_json = json.loads(string_json)
    return HttpResponse(result_json, content_type='application/json')


def getCountryWithLeastDeathsData(request):
    # Find country with least deaths
    dataTable = GetDataTableWithIdentifier(countryWithLeastDeaths, "CountryWithLeastDeaths")
    df = pd.json_normalize(dataTable["data"])
    string_json = df.to_json(orient="records")
    string_json='['+string_json+']'
    result_json = json.loads(string_json)

    return HttpResponse(result_json, content_type='application/json')


def CasesForCountryTillNowFromDatabasePlot(request, case, country):
    country = country.lower()
    url_part, status, = switchForCase(case)
    dataTable = GetDataTableWithIdentifier(casesForCountry, country)

    df = pd.json_normalize(dataTable["data"])
    buffer = plotCreator(country, status, status, "Date", df)

    return HttpResponse(buffer.getvalue(), content_type="image/png")

def DeathAndRecoveryForCountryTillNowFromDatabasePlot(request, country,n):
    country = country.lower()
    dataTable = GetDataTableWithIdentifier(casesForCountry, country)

    df = pd.json_normalize(dataTable["data"])
    buffer = piePlotCreator(country,df,"Deaths","Recovery",n)

    return HttpResponse(buffer.getvalue(), content_type="image/png")

def CasesForCountryTillNowFromDatabaseData(request, case, country):
    country = country.lower()
    url_part, status, = switchForCase(case)
    dataTable = GetDataTableWithIdentifier(casesForCountry, country)

    df = pd.json_normalize(dataTable["data"])
    cases = ["Deaths", "Recovered", "Confirmed"]
    cases.remove(status)
    for caseForCountry in cases:
        df = df.drop([caseForCountry], axis=1)
    string_json = df.to_json(orient="records")
    result_json = json.loads(string_json)
    return JsonResponse(result_json, safe=False)


def getAllCasesForCountry(request, country):
    country = country.lower()

    data = GetDataTableWithIdentifier(casesForCountry, country)

    df = pd.json_normalize(data["data"])
    string_json = df.to_json(orient="records")
    result_json = json.loads(string_json)
    return JsonResponse(result_json, safe=False)


def compare_countries_by_case_plot(request, case, first_country, second_country):
    first_country = first_country.lower()
    second_country = second_country.lower()
    url_part, status, = switchForCase(case)
    first_country_data_table = GetDataTableWithIdentifier(casesForCountry, first_country)
    second_country_data_table = GetDataTableWithIdentifier(casesForCountry, second_country)

    first_country_df = pd.json_normalize(first_country_data_table["data"])
    second_country_df = pd.json_normalize(second_country_data_table["data"])
    buffer = create_two_countries_plot(first_country, second_country, status, status, "Date", first_country_df,
                                       second_country_df)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def compare_countries_by_case(request, case, first_country, second_country):
    first_country = first_country.lower()
    second_country = second_country.lower()
    url_part, status, = switchForCase(case)

    first_country_data_table = GetDataTableWithIdentifier(casesForCountry, first_country)
    second_country_data_table = GetDataTableWithIdentifier(casesForCountry, second_country)

    first_country_df = pd.json_normalize(first_country_data_table["data"])
    second_country_df = pd.json_normalize(second_country_data_table["data"])
    first_country_df=first_country_df[["Country",status,"Date"]].copy()
    second_country_df=second_country_df[["Country",status,"Date"]].copy()
    merge=[first_country_df,second_country_df]
    result=pd.concat(merge)
    string_json=result.to_json(orient="records")
    result_json = json.loads(string_json)
    return JsonResponse(result_json, safe=False)
