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
import time
from django.http import JsonResponse

from DjangoDB.Tables import listOfCountries, countryWithMostDeaths, Cases, basic_date, casesForCountry, \
    countryWithLeastDeaths
from DjangoDB.databaseConnector import updateOrCrateDataTable, updateOrCrateDataTableWithIdentifier, getDatabase, \
    GetDataTableWithIdentifier, updateOrCrateDataTableWithIdentifierWithDb
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




Sure, here's a refactored version of the code:

python
Copy code
import requests
import json
import pandas as pd

def countryWithMostDeathsData(request):
    response = requests.get("https://api.covid19api.com/summary")
    data = response.json()
    countries = data["Countries"]
    # Convert JSON data to pandas dataframe
    df = pd.json_normalize(countries)
    # Find country with highest deaths
    highest_deaths = df.loc[df['TotalDeaths'].idxmax()]
    # Create result dictionary
    result_dict = {'Country': highest_deaths['Country'], 'death_Cases': highest_deaths['TotalDeaths']}
    # Convert dictionary to JSON string
    result_json = json.dumps(result_dict)
    # Update or create data table with result JSON
    updateOrCrateDataTableWithIdentifier(countryWithMostDeaths, result_json, countryWithMostDeaths)
    # Return JSON response with proper content type
    return HttpResponse(result_json, content_type='application/json')

def countryWithLeastDeathsData(request):
    response = requests.get("https://api.covid19api.com/summary")
    data = response.json()
    countries = data["Countries"]

    # Find country with least deaths
    least_deaths = min(countries, key=lambda c: c['TotalDeaths'])

    # Create result dictionary
    result_dict = {'Country': least_deaths['Country'], 'death_Cases': least_deaths['TotalDeaths']}

    # Convert dictionary to JSON string
    result_json = json.dumps(result_dict)
    # Return JSON response with proper content type
    updateOrCrateDataTableWithIdentifier(countryWithLeastDeaths, result_json, countryWithMostDeaths)

    return HttpResponse(result_json,content_type='application/json')



def CasesForCountryTillNowFromDatabasePlot(request, case, country):
    country = country.lower()
    url_part, status, = switchForCase(case)
    dataTable = GetDataTableWithIdentifier(casesForCountry, country)

    df = pd.json_normalize(dataTable["data"])
    buffer = plotCreator(country, status, status, "Date", df)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def CasesForCountryTillNowFromDatabaseData(request, case, country):
    country = country.lower()
    url_part, status, = switchForCase(case)
    dataTable = GetDataTableWithIdentifier(casesForCountry, country)

    df = pd.json_normalize(dataTable["data"])
    cases=["Deaths","Recovered","Confirmed"]
    cases.remove(status)
    for caseForCountry in cases:
        df=df.drop([caseForCountry], axis=1)
    resultJson=df.to_json(orient="records")
    return JsonResponse(json.loads(resultJson), safe=False)


def getAllCasesForCountryToDatabase(request, country):
    country = country.lower()
    day, month, year = getCurrentDayMonthYear()
    url = f'https://api.covid19api.com/country/' + country + f'?from=2020-03-01T00:00:00Z&to=' + str(year) + '-0' + str(month) + '-' + str(day) + 'T00:00:00Z'
    print(url)
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)
    df = df.drop(["CountryCode", "Province", "City", "CityCode", "Lat", "Lon"], axis=1)
    json_str = df.to_json(orient="records")

    updateOrCrateDataTableWithIdentifier(nameOfCollection=casesForCountry, dataToUpload= json.loads(json_str), name= country)
    result_json = {"data":[f"Confirmed, Deaths, Recovered cases for {country}, correctly saved to database"]}
    return JsonResponse(result_json, safe=False)

