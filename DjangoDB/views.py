from django.shortcuts import render
import requests
from .models import Country
import urllib, json
from django.http import JsonResponse
import pandas as pd
from dateutil import parser
from pymongo import MongoClient

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
    countries = pd.DataFrame(data["Countries"])
    listofCounteirs=countries["Country"]
    json_str = json.loads(listofCounteirs.to_json(orient='values'))
    strs='{countries:'+str(json_str)+'}'
    print(strs)
    # js=json.loads(strs)
    # dbname = get_database()
    # collection_name = dbname["ListOfCountries"]
    # collection_name.insert_one(strs)


    return JsonResponse(strs,safe=False)
