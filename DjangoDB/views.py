import requests
import urllib, json
from django.http import JsonResponse
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId


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
    listofCounteirs = countries["Country"]
    json_str = json.loads(listofCounteirs.to_json(orient='values'))
    strs = '{countries:' + str(json_str) + '}'

    countries = [c['Country'] for c in data['Countries']]
    new_data = {"countries": countries}
    print(new_data)

    json_data = json.dumps(new_data)
    data_dict = json.loads(json_data)

    dbname = get_database()
    collection_name = dbname["ListOfCountries"]
    collection_name.insert_one({"_id": str(ObjectId()), "data": data_dict})

    return JsonResponse(new_data, safe=False)
