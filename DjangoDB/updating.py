import json
from datetime import datetime

import requests

import pandas as pd
import time
from django.http import JsonResponse, HttpResponse

from DjangoDB.Tables import listOfCountries, updateList, casesForCountry, slugOfCountries
from DjangoDB.databaseConnector import GetDataTableWithIdentifier, getDatabase, \
    updateOrCrateDataTableWithIdentifierWithDb, updateOrCrateDataTableWithIdentifierAndTimestampWithDb, \
    updateOrCrateDataTableWithIdentifier, GetDataUpdateTableWithIdentifierAndCase, \
    updateOrCrateDataTableWithIdentifierAndCase
from DjangoDB.helpers import getCurrentDayMonthYear, deleteAllParenthese

def getSlugList():
    response = requests.get("https://api.covid19api.com/countries")
    data = response.json()
    slug = [c['Slug'] for c in data]
    new_data = {"Slug": slug}
    json_data = json.dumps(new_data)
    data_dict = json.loads(json_data)
    updateOrCrateDataTableWithIdentifier(listOfCountries, data_dict, slugOfCountries)



def keepUpdatingDatabase():
    getSlugList()
    data=GetDataTableWithIdentifier(listOfCountries,slugOfCountries)["data"]
    data_dict = json.loads(json.dumps(data))
    db=getDatabase()
    countries = data_dict['Slug']
    DELAY = 1  # seconds
    for country in countries:
        if checkToUpdate(country):
            country = deleteAllParenthese(country)
            day, month, year = getCurrentDayMonthYear()
            url = f'https://api.covid19api.com/country/' + country + f'?from=2020-03-01T00:00:00Z&to=' + str(
                year) + '-0' + str(month) + '-' + str(day) + 'T00:00:00Z'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                df = pd.json_normalize(data)
                columns_to_drop = ["CountryCode", "Province", "City", "CityCode", "Lat", "Lon"]
                for col in columns_to_drop:
                    if col in df.columns:
                        df = df.drop(col, axis=1)
                json_str = df.to_json(orient="records")
                #print("update:",url,"\n",country,case)
                updateTimestampForCountry(db,country)
                updateOrCrateDataTableWithIdentifierAndTimestampWithDb(db, casesForCountry, json.loads(json_str), country.lower())
            else:
                print(f"Error fetching data for {country}: {response.status_code}")
            time.sleep(DELAY)

def crateTodayUpdateList():
    getSlugList()
    data=GetDataTableWithIdentifier(listOfCountries,slugOfCountries)["data"]
    data_dict = json.loads(json.dumps(data))
    db=getDatabase()
    countries = data_dict['Slug']
    for country in countries:
        updateTimestampForCountry(db,country)
def updateTimestampForCountry(db,country):
    new_data = [{"lastUpdated": str(datetime.now()),"name": country}]
    json_data = json.dumps(new_data)
    data_dict = json.loads(json_data)
    updateOrCrateDataTableWithIdentifierAndCase(db,updateList, data_dict, country)

def hasAllCountriesBeenUpdated():
    db=getDatabase()
    col=db.get_collection(updateList)
    size=col.count_documents({})
    dataCataloque=col.find_one({"_name": updateList})["data"]
    for data in dataCataloque:
        if datetime.now().date()!=datetime.strptime(data["lastUpdated"],"%Y-%m-%d %H:%M:%S.%f").date():
            return False

    return True

def checkToUpdate(country):
    update_country=GetDataUpdateTableWithIdentifierAndCase(updateList,country)
    if update_country is None:
        return True
    df = pd.json_normalize(update_country["data"])
    date1=datetime.strptime(df["lastUpdated"][0], "%Y-%m-%d %H:%M:%S.%f")
    if date1.date() != datetime.now().date():
        return True
    else:
        return False

