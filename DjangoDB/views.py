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
    countries = [c['Country'] for c in data['Countries']]
    new_data = {"countries": countries}
    json_data = json.dumps(new_data)
    data_dict = json.loads(json_data)
    dbname = get_database()
    collection = dbname['ListOfCountries']
    count = collection.count_documents({})

    print(dbname.list_collection_names())
    count = collection.count_documents({})
    if count > 0:
        cursor = collection.find()
        # print(json.loads(json.dumps(cursor[0]))['_id'])
        collection_name = dbname["ListOfCountries"]
        # print(cursor[0]["_id"])
        # update
        collection_name.update_one({"_id":cursor[0]["_id"]},{'$set': {"data": data_dict}})
    else:
        collection_name = dbname["ListOfCountries"]
        # new Table
        collection_name.insert_one({"_id": str(ObjectId()), "data": data_dict})

    return JsonResponse(data_dict, safe=False)
