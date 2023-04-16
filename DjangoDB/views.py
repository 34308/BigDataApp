import requests
import urllib, json
from django.http import JsonResponse, HttpResponse
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse

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

# def covidPlot(request):
#     url = "https://api.covid19api.com/total/dayone/country/poland"
#     data = requests.get(url).json()
#     df = pd.json_normalize(data)
#
#     fig, ax = plt.subplots()
#     ax.plot(df["Date"], df["Confirmed"])
#     ax.set_title("COVID-19 Confirmed Cases in Poland")
#     ax.set_xlabel("Date")
#     ax.set_ylabel("Confirmed Cases")
#
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     plt.close(fig)
#
#     return HttpResponse(buffer.getvalue(), content_type="image/png")

def covidPlot(request, country):
    url = f'https://api.covid19api.com/total/dayone/country/{country}'
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)

    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Confirmed"])
    ax.set_title("COVID-19 Confirmed Cases in "+country)
    ax.set_xlabel("Date")
    ax.set_ylabel("Confirmed Cases")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)

    return HttpResponse(buffer.getvalue(), content_type="image/png")
