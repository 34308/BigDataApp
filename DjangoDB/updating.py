import json
from datetime import datetime

import requests

import pandas as pd
import time
from django.http import JsonResponse, HttpResponse

from DjangoDB.Tables import listOfCountries, updateList
from DjangoDB.databaseConnector import GetDataTableWithIdentifier, getDatabase, \
    updateOrCrateDataTableWithIdentifierWithDb, updateOrCrateDataTableWithIdentifierAndTimestampWithDb, \
    updateOrCrateDataTableWithIdentifier, GetDataUpdateTableWithIdentifierAndCase, \
    updateOrCrateDataTableWithIdentifierAndCase
from DjangoDB.helpers import switchForCase, getCurrentDayMonthYear


def keepUpdatingDatabase():
    data=GetDataTableWithIdentifier(listOfCountries,listOfCountries)["data"]
    data_dict = json.loads(json.dumps(data))
    db=getDatabase()
    countries = data_dict['countries']
    DELAY = 5  # seconds
    for country in countries:
        cases = ["confirmed", "death", "recovered"]
        for case in cases:
            if checkToUpdate(case,country):
                url_part, status, table = switchForCase(case)
                day, month, year = getCurrentDayMonthYear()
                url = f'https://api.covid19api.com/country/{country}/status/{url_part}/live?from=2020-03-01T00:00:00Z&to={year}-{month}-{day}T00:00:00Z'
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    df = pd.json_normalize(data)
                    columns_to_drop = ["CountryCode", "Province", "City", "CityCode", "Lat", "Lon"]
                    for col in columns_to_drop:
                        if col in df.columns:
                            df = df.drop(col, axis=1)
                    json_str = df.to_json(orient="records")
                    print("update:",url,"\n",country,case)
                    updateTimestampForCountry(case,country)
                    updateOrCrateDataTableWithIdentifierAndTimestampWithDb(db,table, json.loads(json_str), country.lower())
                else:
                    print(f"Error fetching data for {country}: {response.status_code}")
                time.sleep(DELAY)


def updateTimestampForCountry(case,country):
    new_data = {"lastUpdated": str(datetime.now())}
    json_data = json.dumps(new_data)
    data_dict = json.loads(json_data)
    updateOrCrateDataTableWithIdentifierAndCase(updateList, data_dict, country,case)

def checkToUpdate(case,country):
    update_country=GetDataUpdateTableWithIdentifierAndCase(updateList,country,case)
    if update_country is None:
        return True
    df = pd.json_normalize(update_country["data"])
    date1=datetime.strptime(df["lastUpdated"][0], "%Y-%m-%d %H:%M:%S.%f")
    if date1.date() != datetime.now().date():
        return True
    else:
        return False

