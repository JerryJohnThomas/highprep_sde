from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd;
import time 
import requests
import csv
import numpy as np;
import json
# from maps_route_api import api_call
from datetime import datetime as dt
import googlemaps
import gmaps


# endpoint to return the lat-long of the places from the google maps 
class LatLongView(APIView):
    def get(self, request):
        return Response("This is api to return the latitute and longitude of the places that are given");





# endpoint to upload the excel sheet 
class UploadExcelSheetView(APIView):
    def post(self, request):
        print(request.data);
        data = request.data;
        print(data.items);

        print(request.FILES);

########################################################################################################
        # TODO 
            # 1. fetch the excel sheet from the frontend from warehouse guy 
            # 2. store this in database 
########################################################################################################


        return Response("endpoint to upload the excel sheet to store this in db")




def api_call_dummy(a,b):
    size1 = len(a)
    size2 = len(b)
    ans1 = np.random.rand(size1,size2)
    ans2 = np.random.rand(size1,size2)
    return ans1, ans2

def api_call(origins, destinations):
    # origins is an array where each item is an aarray [index, latitiude ,longitide]
    size1 = len(origins)
    size2 = len(destinations)
    
    distance_res = np.zeros([size1,size2])
    time_res = np.zeros([size1,size2])

    body = { "origins": [], "destinations" : [], "travelMode": "DRIVE",
    #   "routingPreference": "TRAFFIC_AWARE"        ## uncommenting this will make the api higher priced and can do a max of 10 points as opposed to 25 points in a singel call
    }

    for location in origins:
        body['origins'].append({"waypoint": {"location": {"latLng": {"latitude": location[1], "longitude": location[2]}}}})
    
    for location in destinations:
        body['destinations'].append({"waypoint": {"location": {"latLng": {"latitude": location[1], "longitude": location[2]}}}})

    print("origin 23", origins[23])
    print("origin 23", origins[24])
    print("destination 13", origins[13])

    # print(body)

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': 'AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g',
        'X-Goog-FieldMask': 'originIndex,destinationIndex,duration,distanceMeters,status,condition',
    }

    call = requests.post('https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix', json=body, headers=headers)
    res = call.text

    print(call.status_code, call.reason)
    json_object = json.loads(call.text)

    print(len(json_object))
    for id,data in enumerate(json_object):
        # print(id, data)
        print(data)
        ind1 = data["originIndex"]
        ind2 = data["destinationIndex"]

        time = int(data["duration"][:-1])


        if ind1 == ind2 or time==0:
            dist = 0
        else:
            dist = data["distanceMeters"]

        distance_res[ind1][ind2] = dist
        time_res[ind1][ind2] = time

    return distance_res , time_res



gmaps = googlemaps.Client(key='AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g')

def get_geocordinates_not_working(place):

    place= place.replace(" ", "+ ")
    url = "https://discover.search.hereapi.com/v1/discover?at=12.7307999,77.9973085&limit=2&q="+place+"&apiKey=6QNNTzC1zysibIBzUnTnBAg5KY1Qc4BBEBElSnrMvSo"

    response = requests.get(url)

    if response.status_code == 200:    # Check if request was successful
        data = response.json()         # Get JSON result
        title = data['items'][0]['title']
        geo = data['items'][0]['position']
        lat = geo['lat']
        lng = geo['lng']
        print("title: ", title)
        print("lat: ", lat)
        print("lng: ", lng)

        return lat, lng, title
    return 1000, 1000, "NIL" 


def get_geocordinates(data):

    place = data.replace(" ", "+ ")
    geocode_result= gmaps.geocode(place)
    lat = geocode_result[0]['geometry']['location'] ['lat']
    lng = geocode_result[0]['geometry']['location'] ['lng']
    print("lat: ", lat)
    print("lng: ", lng)
    return lat, lng, place
    
def rupesh_test1():

    place="palakkad"    
    geocode_result= gmaps.geocode(place)
    lat = geocode_result[0]['geometry']['location'] ['lat']
    lng = geocode_result[0]['geometry']['location'] ['lng']
    print(lat);
    print(lng);
    return lat, lng, place
    


# defining the function to convert the address to lat long 
def addressToLocations(excelPath):
    
    data = pd.read_excel(excelPath)
    places = data['address']
    limit = 218
    data["lat"] =-1.00
    data["lng"] =-1.00

    for i in range(places.size):
        x =places[i]
        lat, lng, title = get_geocordinates(x)
        print(title)
        if lat==1000:
            continue
        print()
        data['lat'][i]= lat
        data['lng'][i]= lng
        time.sleep(1)
        print(i," over")

    data.to_csv("./data/bangalore_dispatch_address_finals_out.csv")



# function to get the distance time matrix 
def calculateDistanceTimeMatrix(filePath):
    
    df = pd.read_csv(filePath)
    lat = df["lat"]
    lng = df["lng"]

    size=lat.size

    print()

    num_index = np.arange(0,size)

    places = []
    for i in range(size):
        places.append([i,lat[i],lng[i]])

    batches = []
    count=0
    for i in range(0,size,25):
        batches.append(places[i:min(i+25,size)])


    arr = np.arange(0,size) 
    dist_mat = pd.DataFrame( index=arr, columns=arr)
    time_mat = pd.DataFrame( index=arr, columns=arr)

    print("total batches ", len(batches))

    for id_i,data_i in enumerate(batches):
        id_range_i = np.arange(id_i*25, id_i*25 + len(data_i))
        
        for id_j,data_j in enumerate(batches):
            id_range_j = np.arange(id_j*25, id_j*25 + len(data_j))
            
            # print(id_range_i," XX ",id_range_j)
            dist_batch, time_batch = api_call(data_i,data_j)
            # updaing the csv
            for j in id_range_j:
                for i in id_range_i:
                    # print("accessing indices", i-id_range_i[0])
                    key_i = i-id_range_i[0]
                    key_j = j-id_range_j[0]
                    dist_mat.at[int(i),str(j)] = dist_batch[key_i][key_j]
                    time_mat.at[int(i),str(j)] = time_batch[key_i][key_j]
            time.sleep(15)
            print(id_i," and ",id_j," is over")

    time_now = dt.now().isoformat()
    time_now= time_now.replace(":",".")

    write_csv=True

    if write_csv:
        dist_mat.to_csv("distance_matrix"+str(size)+"_"+time_now+".csv", index=False)
        time_mat.to_csv("time_matrix"+str(size)+"_"+time_now+".csv", index=False)



# endpoint to start the algorithm once warehouse guy presses start algo 
class StartAlgoView(APIView):
    # post request to start the algo 
    def post(self, request):
        # excelPath = "./data/bangalore_dispatch_address_finals.xlsx"
        # addressToLocations(excelPath)
        filePath = "./data/bangalore_dispatch_address_finals_out.csv";
        calculateDistanceTimeMatrix(filePath)

        # rupesh_test1();
########################################################################################################
        # TODO
            # 1.fetch the excel sheet consisting of the list of places and the available rider 
            # 2. find the (lat, long) for each of the places, distance and time matrix using google maps apis
            # 3. then these points will be feed to the algorithm 
            # 4. wait for the algorithm to return the final result 
            # 5. once got the final result find the routes of each destination for each rider.
            # 6. store this in database.(why ??)
            # 7. then return the direction routes with rider id to the frontend or warehouse guy to be specific.
            # 8. also notify each rider about the directions routes that needs to be navigated.(this is the current issue how are we going to do that).
        # main problems will be to 

###########################################################################################################
        return Response("hopefully should be done ");


