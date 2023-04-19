import requests
import urllib, json
from django.http import JsonResponse, HttpResponse
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId

import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse
import datetime

def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://User2:QIHSchL8W0aQ5Uqb@bigdatadatabase.vatkkvd.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['BigDataDataBase']


def ListOfCountriesWichWeHaveDataOn(request):
    response = requests.get("https://api.covid19api.com/summary")
    data = response.json()
    countries = [c['Country'] for c in data['Countries']]
    new_data = {"countries": countries}
    json_data = json.dumps(new_data)
    data_dict = json.loads(json_data)
    dbname = get_database()
    collection = dbname['ListOfCountries']

    count = collection.count_documents({})
    if count > 0:
        cursor = collection.find()
        collection_name = dbname["ListOfCountries"]
        # update
        collection_name.update_one({"_id": cursor[0]["_id"]}, {'$set': {"data": data_dict}})
    else:
        collection_name = dbname["ListOfCountries"]
        # new Table
        collection_name.insert_one({"_id": str(ObjectId()), "data": data_dict})

    return JsonResponse(data_dict, safe=False)

def getCurrentDayMonthYear():
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    return day,month,year
def CounrtyWithMostDeaths(request):
    day,month,year=getCurrentDayMonthYear()
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

def updateOrCrateDataTable(nameOfCollection,dataToUpload):
    dbname = get_database()
    collection = dbname[nameOfCollection]

    count = collection.count_documents({})
    if count > 0:
        cursor = collection.find()
        collection_name = dbname[nameOfCollection]
        # update
        collection_name.update_one({"_id": cursor[0]["_id"]}, {'$set': {"data": dataToUpload}})
    else:
        collection_name = dbname[nameOfCollection]
        # new Table
        collection_name.insert_one({"_id": str(ObjectId()), "data": dataToUpload})
def updateOrCrateDataTableWithIdentifier(nameOfCollection,dataToUpload,name):
    dbname = get_database()
    collection = dbname[nameOfCollection]
    results= collection.find_one({"_name":name})

    if results:

        collection_name = dbname[nameOfCollection]
        # update
        collection_name.update_one({"_id": results["_id"],"_name":name}, {'$set': {"data": dataToUpload}})
    else:

        collection_name = dbname[nameOfCollection]
        # new Table
        collection_name.insert_one({"_id": str(ObjectId()),"_name":name, "data": dataToUpload})

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

    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Cases"])
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
    ax.plot(df["Date"], df["Confirmed"])
    ax.set_title("COVID-19 Confirmed Cases in " + country)
    ax.set_xlabel("Date")
    ax.set_ylabel("Confirmed Cases")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)

    return HttpResponse(buffer.getvalue(), content_type="image/png")
