from datetime import datetime

import pandas as pd
import requests
import urllib, json
from django.http import JsonResponse, HttpResponse
from pymongo import MongoClient
from bson import ObjectId


def getDatabase():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://User2:QIHSchL8W0aQ5Uqb@bigdatadatabase.vatkkvd.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['BigDataDataBase']


def updateOrCrateDataTable(nameOfCollection, dataToUpload):
    dbname = getDatabase()
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


def updateOrCrateDataTableWithIdentifier(nameOfCollection, dataToUpload, name):
    dbname = getDatabase()
    collection = dbname[nameOfCollection]
    results = collection.find_one({"_name": name})

    if results:

        collection_name = dbname[nameOfCollection]
        # update
        collection_name.update_one({"_id": results["_id"], "_name": name}, {'$set': {"data": dataToUpload}})
    else:

        collection_name = dbname[nameOfCollection]
        # new Table
        collection_name.insert_one({"_id": str(ObjectId()), "_name": name, "data": dataToUpload})
    dbname.client.close()


def updateOrCrateDataTableWithIdentifierWithDb(dbname, nameOfCollection, dataToUpload, name):
    collection = dbname[nameOfCollection]
    results = collection.find_one({"_name": name})

    if results:

        collection_name = dbname[nameOfCollection]
        # update
        collection_name.update_one({"_id": results["_id"], "_name": name}, {'$set': {"data": dataToUpload}})
    else:

        collection_name = dbname[nameOfCollection]
        # new Table
        collection_name.insert_one({"_id": str(ObjectId()), "_name": name, "data": dataToUpload})


def updateOrCrateDataTableWithIdentifierAndTimestampWithDb(dbname, nameOfCollection, dataToUpload, name):
    collection = dbname[nameOfCollection]
    results = collection.find_one({"_name": name})

    if results:

        collection_name = dbname[nameOfCollection]
        # update
        collection_name.update_one({"_id": results["_id"], "_name": name, "_lastUpdated": datetime.now()},
                                   {'$set': {"data": dataToUpload}})

    else:

        collection_name = dbname[nameOfCollection]
        # new Table
        collection_name.insert_one(
            {"_id": str(ObjectId()), "_name": name, "_lastUpdated": datetime.now(), "data": dataToUpload})



def updateOrCrateDataTableWithIdentifierAndCase( dbname,nameOfCollection, dataToUpload, name):
    collection = dbname[nameOfCollection]
    results = collection.find_one({"_name": nameOfCollection})
    results2 = collection.find_one({"_name": nameOfCollection,"data.name": name})
    if results:
        collection_name = dbname[nameOfCollection]
        # update
        if results2:
            data=results2["data"]

            df = pd.DataFrame(data,columns=data[0].keys())
            index = df.index[df['name'] == name]
            collection_name.update_one({"_id": results2["_id"]},
                                        {'$set': {f"data.{index[0]}.lastUpdated":  str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))}})
        else:

            collection_name.update_one({"_id": results["_id"]},{'$push': {"data": {"lastUpdated": str(datetime.now()),"name": name}}})
    else:
        collection_name = dbname[nameOfCollection]
        # new Table
        collection_name.insert_one(
            {"_id": str(ObjectId()), "_name": nameOfCollection, "data": dataToUpload})


def GetDataTableWithIdentifier(nameOfCollection, name):
    dbname = getDatabase()
    collection = dbname[nameOfCollection]
    results = collection.find_one({"_name": name})

    if results:
        # update
        dbname.client.close()
        return results
    else:
        raise Exception("No such table")
def GetDataTable(nameOfCollection):
    dbname = getDatabase()
    collection = dbname[nameOfCollection]

    if collection:
        # update
        dbname.client.close()
        return collection
    else:
        raise Exception("No such table")

def GetDataUpdateTableWithIdentifierAndCase(nameOfCollection, country):
    dbname = getDatabase()
    collection = dbname[nameOfCollection]
    results = collection.find_one({"_name": country})

    if results:
        # update
        dbname.client.close()
        return results
    else:
        return None
