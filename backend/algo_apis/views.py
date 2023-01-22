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
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import AlgorithmStatusModelSerializer
from .models import AlgorithmStatusModel, Location, Rider
from login_apis.models import PersonInfo
# import random
import string
import random
from .Think import think

# endpoint to return the lat-long of the places from the google maps 
class LatLongView(APIView):
    def get(self, request):
        return Response("This is api to return the latitute and longitude of the places that are given");



def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# endpoint to upload the excel sheet 
class UploadExcelSheetView(APIView):
    def post(self, request):
        print(request.data);
        print(request.FILES);
        data = request.data;
        token = data['token'];
        file = request.FILES['file']

        
        

        randomNumber = random_string_generator()
        print(randomNumber)

        print("The token that i got is \n", token);
        print("The file name that i got is \n", file);
        excelData = pd.read_excel(file);

        print("The content of the file is ", excelData);

        userName = Token.objects.get(key=token).user
        currentUser = PersonInfo.objects.get(email = str(userName))
        print('The token belongs to the following user\n\n', currentUser);
        userName = currentUser.email;

        data2 = {}
        data2['username'] = userName
        data2['random_number'] = randomNumber
        data2['status'] = "NotFinished"
        data2['excelSheetFile'] = file;

        

        # serializedData = AlgorithmStatusModelSerializer(data=data2, file=request.FILES);
        algorithmStatus = AlgorithmStatusModel.objects.create(username= userName, random_number = randomNumber, status="Not Started", excelSheetFile = file)

        algorithmStatus.save();
        print("The saved new entry in the algorithm thing is \n", algorithmStatus);
        
        # say everything went fine 
        return Response({"msg" : "Hopefully done successfully", "randomNumber" : randomNumber}, status=status.HTTP_201_CREATED)



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

    # print("origin 23", origins[23])
    # print("origin 23", origins[24])
    # print("destination 13", origins[13])

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
def addressToLocations(excelPath, userName, randomNumber):
    
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
    latLongCsvFilePath = "./data/" + str(userName) + "_" + str(randomNumber) + ".csv"
    print("The path of the geo_encoding with lat long coordinates is ", latLongCsvFilePath);
    # data.to_csv("./data/bangalore_dispatch_address_finals_out.csv")
    data.to_csv(latLongCsvFilePath);



# function to get the distance time matrix 
def calculateDistanceTimeMatrix(filePath, userName, randomNumber):
    
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
    distMatrixFileName = "distance_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
    timeMatrixFileName = "time_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
    if write_csv:
        dist_mat.to_csv(f"./data/distance/{distMatrixFileName}", index=True)
        time_mat.to_csv(f"./data/time/{timeMatrixFileName}", index=True)


def storeLatLongInDb(latLongCsvFilePath, userName, randomNumber, currentUser):

        df = pd.read_csv(latLongCsvFilePath)
        lat = df["lat"]
        lng = df["lng"]
        print("The lat is ",type(lat));
        print("The long is ",type(lng));

        # latitude = [];
        # longitude = [];
        coordinates = [];

        # using the for loop for this purpose 
        for i in range(lat.size):
            coordinates.append([i+1, df['lat'][i], df['lng'][i]])


        location_names = [];

        # converting these data into json 
        locationArray = {
            "coordinates" : coordinates,
            "location_names" : location_names
        }
        currentLocationEntry = Location.objects.create(username = currentUser.email, random_number = randomNumber, location_array = locationArray)
        currentLocationEntry.save();

        print("The new entry is as follows\n\n", currentLocationEntry);



# function to find the first n available riders for this purpose 
def findFirstNAvailableRiders():
    riders = Rider.objects.filter(status = "NotAvailable").only("email");

    availableRiders = []

    for rider in riders.iterator():
        availableRiders.append(rider.email)
    # using the for loop for this purpose 
    # for i in range(riders.size):
    #     if riders[i].status == "NotAvailable":
    #         availableRiders.append(riders[i])

    # print("The list of all riders are as follows \n", riders);

    # say everything went fine 
    return availableRiders


# endpoint to start the algorithm once warehouse guy presses start algo 
class StartAlgoView(APIView):
    # post request to start the algo 
    def post(self, request):
        # first we have to make the status as started 
        token = request.data['token'];
        randomNumber = request.data['randomNumber']

        # find the entry on this random number 
        userName = Token.objects.get(key=token).user
        currentUser = PersonInfo.objects.get(email = str(userName))
        currentAlgorithm = AlgorithmStatusModel.objects.get(random_number = randomNumber, username=userName);
        print("The current algorith excel sheet model is ", currentAlgorithm);
        print("The current user is  ", currentUser);

        # updating the status 
        currentAlgorithm.status = "Started";
        currentAlgorithm.save();

########################################################################################################
        #TODO 
            # find the list of first n available riders from the database and store with id starting with 1 
        availableRidersN = findFirstNAvailableRiders();
        print("The available riders are as follows :", availableRidersN);


########################################################################################################

        excelPath = currentAlgorithm.excelSheetFile;


########################################################################################################
        #TODO ==> UNCOMMENT THE LINE 
        # addressToLocations(excelPath, userName, randomNumber)
########################################################################################################

        # excelData = pd.read_excel(excelPath);
        
        # latLongCsvFilePath is the file in which the lat and long has been find out by the algorithm 
        latLongCsvFilePath = "./data/" + str(userName) + "_" + str(randomNumber) + ".csv"
        # storeLatLongInDb(latLongCsvFilePath, userName, randomNumber, currentUser)

########################################################################################################
        #TODO 
            # how to find the places given the latitude and longitude 

            # now we have to calculate the distance time matrix csv for the algorithm 
            # calculateDistanceTimeMatrix(latLongCsvFilePath, userName, randomNumber);
########################################################################################################

        distMatrixFileName = "./data/distance/distance_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
        # timeMatrixFileName = "./data/time/time_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
        timeMatrixFileName = "./time_matrix218_2023-01-21T17.04.47.497441.csv"
        # now i will be calling the NEEL's algo here 
        # algoRes = think(timeMatrixFileName)

########################################################################################################
        #TODO 
        #   observe the output and find the riders id correctly and locations correctly 
        #   return this to frontend 
########################################################################################################

        # print("The result from the algorithm is ", algoRes);

        return Response({"msg" : "Successfully Started the Algorithm"}, status=status.HTTP_200_OK);


