import copy
import threading
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd;
import time 
import requests
import csv
from algo_apis.pickup import pickup
import numpy as np;
import json
# from maps_route_api import api_call
from datetime import datetime as dt
import googlemaps
import gmaps

from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import AlgorithmStatusModelSerializer,RiderSerializer
from .models import AlgorithmStatusModel, Location, Rider
from login_apis.models import PersonInfo
from rider_apis.models import Bag
from inventory_apis.models import Item
# import random
import string
import random
from .Think import think
from .maps_route_api import api_call_pickup, api_call_pickup_dummy
from .main import solve
from .rudr import *
from .markov_rudr import *
from .func_rudr import *

# endpoint to return the lat-long of the places from the google maps 
class LatLongView(APIView):
    def get(self, request):
        return Response("This is api to return the latitute and longitude of the places that are given");



def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# endpoint to `upload` the excel sheet 
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

        if "location" in excelData.columns:
            for index, row in excelData.iterrows():
                if row['location'] not in row['address']:
                    excelData.at[index, 'address'] = row['address'] + ', ' + row['location']
            
        #save the updated sheet
        excelData.to_excel(file)
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


        # if ind1 == ind2 or time==0:  ## i made a mistake here before
        if time==0:
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
    # place = "MTH, Best of Bengal"
    geocode_result= gmaps.geocode(place)
    print("The result", geocode_result);
    if len(geocode_result)>=1 and 'geometry'in geocode_result[0]:
        lat = geocode_result[0]['geometry']['location'] ['lat']
        lng = geocode_result[0]['geometry']['location'] ['lng']
        print("lat: ", lat)
        print("lng: ", lng)
        return lat, lng, place, 1
    return 0, 0, 0, 0
    





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
    # limit = 218
    data["lat"] =-1.00
    data["lng"] =-1.00

    for i in range(places.size):
        x =places[i]
        lat, lng, title , status= get_geocordinates(x)
        print(title)
        in_india = ((lat >=8 and lat <=40) and (lng >=68 and lng <=96))
        if lat==1000 or status==0 or in_india == False:
            continue
        print()
        data['lat'][i]= lat
        data['lng'][i]= lng
        time.sleep(1)
        print(i," over")
    latLongCsvFilePath = "./data/" + str(userName) + "_" + str(randomNumber) + ".csv"
    print("The path of the geo_encoding with lat long coordinates is ", latLongCsvFilePath);
    data = data[(data["lat"]!=-1) & (data["lng"]!=-1)]

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
                    # i changed str(j) to int(j)
                    dist_mat.at[int(i),int(j)] = dist_batch[key_i][key_j]
                    time_mat.at[int(i),int(j)] = time_batch[key_i][key_j]
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
        # print("The type of item is ", type(i))
        if 'Volume' in df.columns:
            print("Volume column already exists")
        else:
            df['Volume'] = np.random.uniform(low=15000, high=40000, size=(len(df)))

        # print(df)
        # latitude = [];
        # longitude = [];
        coordinates = [];
        # here we will have to create the new item in the database as we are getting it from excel sheet 
        # using the for loop for this purpose 
        for i in range(len(lat)):
            random_string = "item" +  random_string_generator() ;
            newItem = Item.objects.create(item_name = random_string, item_volume = df["Volume"][i])
            coordinates.append([i+1, df['lat'][i], df['lng'][i], newItem.item_name, 0])
            # coordinates.append([i+1, df['lat'][i], df['lng'][i]])


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
def findFirstNAvailableRiders(n):
    riders = Rider.objects.filter(status = "Available").only("email");
    print()
    count = 0;
    availableRiders = []

    for rider in riders.iterator():
        if count == n:
            break
        availableRiders.append(rider.email)
        count = count + 1;
    
    if(count < n):
        # then this means we do not have enough riders to deliver the items 
        return [];
    # say everything went fine 
    return availableRiders





# function to mark the riders as not available 
def markThemAsNonAvailable(availableRidersN):
    for i in range(len(availableRidersN)):
        currRider = Rider.objects.get(email = availableRidersN[i]);
        currRider.status = "NotAvailable";
        currRider.save();

    # say everything went fine 
    return;






# this function will store the list of location_ids assigned to rider in their collection. 
# (location_id is the field)
def storeLocationsInRiderCollection(username, randomNumber, riderIdVsLoc, availableNRiders):
    i = 0;
    riderDict = {};
    # using the for loop for storing this in database 
    for riderEmail in availableNRiders:
        currentRider = Rider.objects.get(email = riderEmail);
        currentRider.location_ids = {
            "coordinates" : riderIdVsLoc[i]
        }
        currentRider.username = username;
        currentRider.random_number = randomNumber
        print("The rider ", riderEmail);
        print("got the coordinates = ", riderIdVsLoc[i]);
        print("\n\n")
        # here we also have to assign the temp id for easy purpose 
        currentRider.temp_id = i;
        currentRider.save();
        riderDict[riderEmail] = riderIdVsLoc[i];
        i = i+1;

    # currentAlgorithm = 
    # saving the locations to be completed by the rider in the AlgorithmStatusModel thingy 
    currentAlgorithm = AlgorithmStatusModel.objects.get(username =  username, random_number = randomNumber);
    currentAlgorithm.rider_to_location = riderDict;
    # we also have to update the status of the algorithm as finished for this purpose
    currentAlgorithm.status = "Finished";
    currentAlgorithm.save();
    # say everything went fine 
    return riderDict;









# function to assign the bags to these riders by creating the new ones for this purpose 
def createBagForEachRiders(availableNRiders):

    # using the for loop to calculate the new bag and store the items to be delivered randomly 
    # for this particular rider 
    for rider in availableNRiders:
        currentRider = Rider.objects.get(email = rider)
        print("The email of the current rider is ", rider);
        # creating new bag 
        newBag = Bag(bag_size = 30, item_list = {"item" : []});
        newBag.save();

        # assigning the new bag to the rider for this particuar tour for this purpose 
        currentRider.bag_id = str(newBag.bag_id);
        # here we also have to add the items into the bag for each of the riders 
        # we have to first get the locations and for each of the location we have to add a item 
        # randomly assign the items to this rider having k locations 
        locationCount = len(currentRider.location_ids["coordinates"]);
        print("The number of coordinates allocated to this particular rider is as follows \n", locationCount);
        itemList = Item.objects.all();
        itemCount = len(itemList)
        k = 0;
        for i in range(locationCount):
            itemListJson = {
                "item_name" : itemList[k].item_name,
                "item_volume" : itemList[k].item_volume
            }
            k = (k+1)%itemCount;
            newBag.item_list["item"].append(itemListJson)
        newBag.save();
        print("The length of the bag items inside the assigned bag is as follows \n\n", len(newBag.item_list["item"]))
        currentRider.save();


    # say everything went fine 
    return;






def find_path_cost(path):
    if len(path) == 0:
        return 0
    temp_path = copy.deepcopy(path)
    temp_path += [temp_path[0]]
    path_sum = 0
    for i in range(len(temp_path)-1):
        path_sum += node_travel_time[temp_path[i]][temp_path[i+1]]
    return path_sum


def find_loc(n, m, node_travel_distance, node_travel_time, node_weights, deliveryManWeight, positions):
	clusters = markov_clusters(node_travel_distance, positions, False)


	print(clusters)

	# starting_points = random.sample(range(1, m+1), n)
	# locations, _ = find_path_for_all_drivers(n, m, node_travel_time, node_weights, deliveryManWeight, starting_points, 20)
	clusters = clusters[1:]
	for i in range(len(clusters)):
		clusters[i] = list(clusters[i])


	best_cost = infinity
	best_locations = {}
	for i in range(100):
		locations, cost = find_travel_clusters(n, m, node_travel_time, copy.deepcopy(
			clusters), node_weights, deliveryManWeight)

		all_path_sum = 0
		for loc in locations.values():
			all_path_sum += find_path_cost(loc)

		cost = max(cost, all_path_sum)

		if cost < best_cost:
			best_locations = locations
			best_cost = cost

	return best_locations, best_cost


# defining the function to find the total number of locations 
def findNumberOfLocations(currentAlgorithm, latLongCsvFilePath):

    with open(latLongCsvFilePath, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    total_entries = len(data)
    # print("The total number of locations are as follows +++++\n\n", totale)
    # print(total_entries-1)

    # say everything went fine 
    return total_entries-1;






# function to find the map of location_id and item weight 
def findNodeWeights(currentLocation):
    coordinates = currentLocation.location_array["coordinates"];

    itemVolumeNodeWeights = {};

    # using the for loop for this purpose 
    for entry in coordinates:
        itemName = entry[3];
        itemVolume = Item.objects.get(item_name = itemName).item_volume
        itemVolumeNodeWeights[entry[0]] = float(itemVolume);


    # say everything went fine 
    return itemVolumeNodeWeights





# defining the function to find the weight of bags of each rider involved in tour 
def findBagWeightsOfRiders(availableNRiders):
    riderVsBagWeight = {}
    for rider in availableNRiders:
        currentRider = Rider.objects.get(email = rider);
        currentBag = Bag.objects.get(bag_id = currentRider.bag_id);
        riderVsBagWeight[currentRider.temp_id] = currentBag.bag_size;
    
    # say everything went fine 
    return riderVsBagWeight;




def long_running_task(n, userName, currentAlgorithm, currentUser, randomNumber):
    ########################################################################################################
        #TODO 
        # n = 5
        # find the list of first n available riders from the database and store with id starting with 1 
        availableNRiders = findFirstNAvailableRiders(n);
        print("The available riders are as follows :", availableNRiders);
        if(availableNRiders == []):
            return Response({"msg" : "Not Enough Riders to deliver"}, status=status.HTTP_403_FORBIDDEN);
        
        # # idMapForRiders = 
        # # now we have to mark these as non available 
        # markThemAsNonAvailable(availableNRiders);

########################################################################################################

        excelPath = currentAlgorithm.excelSheetFile;


########################################################################################################
        #TODO ==> UNCOMMENT THE LINE 
        addressToLocations(excelPath, userName, randomNumber)
########################################################################################################

        # excelData = pd.read_excel(excelPath);
        
        # latLongCsvFilePath is the file in which the lat and long has been find out by the algorithm 
        latLongCsvFilePath = "./data/" + str(userName) + "_" + str(randomNumber) + ".csv"
        storeLatLongInDb(latLongCsvFilePath, userName, randomNumber, currentUser)

########################################################################################################
        #TODO 
            # how to find the places given the latitude and longitude 

            # now we have to calculate the distance time matrix csv for the algorithm 
        calculateDistanceTimeMatrix(latLongCsvFilePath, userName, randomNumber);
########################################################################################################

        distMatrixFileName = "./data/distance/distance_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
        timeMatrixFileName = "./data/time/time_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";

        # here we also have to calculate the total number of locations under this algorithm 
        # and finally save this to db 
        totalLocations = findNumberOfLocations(currentAlgorithm, distMatrixFileName);
        currentAlgorithm.number_of_locations = totalLocations;
        currentAlgorithm.save();
        currentLocation = Location.objects.get(username = userName, random_number = randomNumber)
        # creating the dictionary for item weights 
        locationToItemVolume_nodeWeights = findNodeWeights(currentLocation);
        print("the node item weight is \n\n\n", locationToItemVolume_nodeWeights)

        # deliveryManBagWeight = findBagWeightsOfRiders(availableNRiders);

        # print("the bag weight is \n\n\n", deliveryManBagWeight)
        
        # timeMatrixFileName = "./time_matrix218_2023-01-21T17.04.47.497441.csv"
        # now i will be calling the NEEL's algo here 
        time_matrix_data = think(timeMatrixFileName, n)
        dist_matrix_data = think(distMatrixFileName, n)
        print("The length of matrix", len(dist_matrix_data))

        # node_travel_distance = [[0 for i in range(totalLocations+1)] for j in range(totalLocations+1)]

        # for i in range(totalLocations):
        #     for j in range(i+1, totalLocations):
        #         node_travel_distance[int(points[i][0])][int(
        #             points[j][0])] = 1 / adjMtrxDist[int(points[i][0])][int(points[j][0])]
        #         node_travel_distance[int(points[j][0])][int(
        #             points[i][0])] = 1 / adjMtrxDist[int(points[j][0])][int(points[i][0])]

        
        algoRes, totalCost = solve(n, totalLocations, dist_matrix_data, time_matrix_data, locationToItemVolume_nodeWeights, 640000,0)
        # print("The algo result is as follows \n\n\n", algoRes)
        men = totalCost
        for i in range(100):

            temp, totalCost = solve(n, totalLocations, dist_matrix_data, time_matrix_data, locationToItemVolume_nodeWeights, 640000,0)

            print("iteration ", i , " over");
            # print(totalCost)

            if(totalCost < men):

                totalCost = totalCost

                men = totalCost

                algoRes = temp

        # call rudrs algorithm  continue the minimum 


        print("Final Total Cost : ", totalCost)

########################################################################################################
        #TODO 
        #   observe the output and find the riders id correctly and locations correctly 
        # the output order to Neels algo is place_id vs rider_id
        riderIdVsLoc = [];
        currentLocation = Location.objects.get(username = currentUser.email, random_number = randomNumber);
        location_array = currentLocation.location_array;
        coordinates = location_array['coordinates']
        print("The location_array is as follows \n", coordinates)


        for i in range(n):
            riderIdVsLoc.append([]);

        # here we are assigning the locations to the riders 
        for key in algoRes:
            for location in algoRes[key]:
                riderIdVsLoc[key].append(coordinates[location-1])
            # currentLatLong = coordinates[key-1];
            # riderIdVsLoc[algoRes[key]-1].append(currentLatLong);
        

        # print("The final mapping of riderid vs loc is as follows \n\n");
        # print(riderIdVsLoc)

        riderLocationDict = storeLocationsInRiderCollection(currentUser.email, randomNumber, riderIdVsLoc, availableNRiders);

        # now we also have to create new bag for each of this riders 
        createBagForEachRiders(availableNRiders);


class DummyStart(APIView):
    def post(self, request):
        token = request.data["token"];
        userName = Token.objects.get(key=token).user
        randomNumber = request.data["randomNumber"];
        n = request.data["n"]

        # for the dummy data use the following credentials 
        # token of war1@gmail.com
        # randomNumber = zy2h00iubx

        latLongCsvFilePath = "./data/" + str(userName) + "_" + str(randomNumber) + ".csv"
        # currUser = PersonInfo.objects.get(email)
        currentUser = PersonInfo.objects.get(email = str(userName))
        # storeLatLongInDb(latLongCsvFilePath, userName, randomNumber, currentUser)
        distMatrixFileName = "./data/distance/distance_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
        timeMatrixFileName = "./data/time/time_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
        
        currentAlgorithm = AlgorithmStatusModel.objects.get(username = userName, random_number = randomNumber);
        currentAlgorithm.number_of_drivers = n;
        
        availableNRiders = findFirstNAvailableRiders(n);
        print("The available riders are as follows \n\n\n\n\n", availableNRiders)
        print("The available riders are as follows :", availableNRiders);
        # here we also have to calculate the total number of locations under this algorithm 
        # and finally save this to db 
        totalLocations = findNumberOfLocations(currentAlgorithm, distMatrixFileName);
        print("totalLocations ==> ", totalLocations);
        currentAlgorithm.number_of_locations = totalLocations;
        currentAlgorithm.save();
        currentLocation = Location.objects.get(username = userName, random_number = randomNumber)
        # creating the dictionary for item weights 
        locationToItemVolume_nodeWeights = findNodeWeights(currentLocation);
        print("the node item weight is \n\n\n", locationToItemVolume_nodeWeights)

        # deliveryManBagWeight = findBagWeightsOfRiders(availableNRiders);

        # print("the bag weight is \n\n\n", deliveryManBagWeight)
        
        # timeMatrixFileName = "./time_matrix218_2023-01-21T17.04.47.497441.csv"
        # now i will be calling the NEEL's algo here 
        # n is total number of drivers 
        numberOfDrivers = currentAlgorithm.number_of_drivers;

        time_matrix_data = think(timeMatrixFileName, numberOfDrivers)
        dist_matrix_data = think(distMatrixFileName, numberOfDrivers)
        print( "dist_matrix_data === ", dist_matrix_data)
        print("The length of matric", len(dist_matrix_data))

        print("The number of drivers\n\n", numberOfDrivers);
        print("numberofrivers", numberOfDrivers)
        print("totallocations", totalLocations)
        print("dist_matrix_data", dist_matrix_data)
        print("time_matrix_data", time_matrix_data )
        print("locationToItemVolume_nodeWeights", locationToItemVolume_nodeWeights )
        print("deliveryManWeight  ", 640000 )
        print("n  ", 0 )

        
        algoRes, totalCost = solve(numberOfDrivers, totalLocations, dist_matrix_data, time_matrix_data, locationToItemVolume_nodeWeights, 640000,0)
        # print("The algo result is as follows \n", algoRes)
        men = totalCost
        for i in range(100):

            temp, totalCost = solve(numberOfDrivers, totalLocations, dist_matrix_data, time_matrix_data, locationToItemVolume_nodeWeights, 640000,0)

            debug_string = "";
            for key in temp:
                debug_string+=str(key)+" : "+str(len(temp[key]))+" , "
            print("iteration ", i , " over ::::  ",debug_string);
            # print(totalCost)

            if(totalCost < men):

                totalCost = totalCost

                men = totalCost

                algoRes = temp




        print("Final Total Cost : ", totalCost)

########################################################################################################
        #TODO 
        #   observe the output and find the riders id correctly and locations correctly 
        # the output order to Neels algo is place_id vs rider_id
        riderIdVsLoc = [];
        currentLocation = Location.objects.get(username = currentUser.email, random_number = randomNumber);
        location_array = currentLocation.location_array;
        coordinates = location_array['coordinates']
        print("The location_array is as follows \n", coordinates)


        for i in range(n):
            riderIdVsLoc.append([]);

        # here we are assigning the locations to the riders 
        for key in algoRes:
            for location in algoRes[key]:
                riderIdVsLoc[key].append(coordinates[location-1])
            # currentLatLong = coordinates[key-1];
            # riderIdVsLoc[algoRes[key]-1].append(currentLatLong);
        

        # print("The final mapping of riderid vs loc is as follows \n\n");
        # print(riderIdVsLoc)

        riderLocationDict = storeLocationsInRiderCollection(currentUser.email, randomNumber, riderIdVsLoc, availableNRiders);

        # now we also have to create new bag for each of this riders 
        createBagForEachRiders(availableNRiders);

        return Response({"msg" : "success"}, status=status.HTTP_200_OK)






# endpoint to start the algorithm once warehouse guy presses start algo 
class StartAlgoView(APIView):
    # post request to start the algo 
    def post(self, request):
        # first we have to make the status as started 
        
        token = request.data['token'];
        randomNumber = request.data['randomNumber']
        n = int(request.data["n"]);

        print("the number of riders is ", n);

        # find the entry on this random number 
        userName = Token.objects.get(key=token).user
        currentUser = PersonInfo.objects.get(email = str(userName))
        currentAlgorithm = AlgorithmStatusModel.objects.get(random_number = randomNumber, username=userName);
        print("The current algorith excel sheet model is ", currentAlgorithm);
        print("The current user is  ", currentUser);

        # updating the status 
        currentAlgorithm.status = "Started";
        currentAlgorithm.number_of_drivers = n;
        currentAlgorithm.save();
        my_tuple = (n, userName, currentAlgorithm, currentUser, randomNumber)
        threading.Thread(target=long_running_task, args=my_tuple).start()


        return Response({"msg" : "Successfully Started the Algorithm", "data" : "some"}, status=status.HTTP_200_OK);










# endpoint to check the status of the algorithm running 
class StatusOfAlgo(APIView):
    def post(self, request):
        randomNumber = request.data['randomNumber'];
        print("The random nuber  that is got is ", randomNumber);
        token = request.data['token'];
        print("The token that is got is ", token);
        userName = Token.objects.get(key=token).user

        # getting the current user 
        currentUser = PersonInfo.objects.get(email = str(userName))
        # getting the algorithm given the username and random string 
        currentAlgorithm = AlgorithmStatusModel.objects.get(username = currentUser.email, random_number = randomNumber);

        print("The current algorithm is ", currentAlgorithm);

        currentStatus = currentAlgorithm.status;
        # if the algorithm is complete or finished then we have to send the results back to the frontend 
        if currentStatus == 'Finished':
            # then the algorithm is finished hence we can send back the final result 
            rider_to_locations = currentAlgorithm.rider_to_location;
            ridersInformation = [];

            # do note that in the rider collection the username field will store the username of warehouse 
            # guy who has started the algorithm 
            currentAlgoRiders = Rider.objects.filter(username = userName, random_number = randomNumber)
            for currentRider in currentAlgoRiders:
                currentRiderPersonInfo = PersonInfo.objects.get(email = currentRider.email)
                # currentRider = Rider.objects.get(email = riderEmail);
                currentRiderJson = {
                    "email" : currentRider.email,
                    "name" : currentRiderPersonInfo.name,
                    "status" : currentRider.status,
                    "location_ids" : currentRider.location_ids
                }
                ridersInformation.append(currentRiderJson);
            
            print("The riders information is ", ridersInformation);
            return Response({"msg" : "Algorithm Finished", "rider_to_location" : ridersInformation}, status=status.HTTP_200_OK)


        # say everything went fine 
        return Response({"msg" : "Algo is still going on"}, status=status.HTTP_200_OK); 



# defining the function to find the list of riders involved in this particular algorithm 
def findListOfRidersInvolved(userName, randomNumber):
    result = Rider.objects.filter(username = userName, random_number=randomNumber);
    listOfRiders = [];
    # using the for loop to get the email 
    for rider in result:
        listOfRiders.append(rider.email);
    print("The list of emails of riders involved in this tour are as follows \n");
    print(listOfRiders);

    # say everything went fine 
    return listOfRiders;




# defining the function to remove the item from the list for this purpose 
def removeItemFromBag(currentRider):
    # print("The current rider is ", currentRider);
    # print("The current bag id is ", type(currentRider.bag_id))
    print("The current bag id is ", (currentRider.bag_id))

    bag_id = int(currentRider.bag_id);
    print("The bag_id for this rider is \n", bag_id);

    currentBag = Bag.objects.get(bag_id = bag_id);

    print("The list of items of items in this bag is ", currentBag.item_list["item"]);
    print('The length of this item list is \n', len(currentBag.item_list["item"]));

    # deleting this item at this particular index 
    itemList =  currentBag.item_list["item"];
    itemList = itemList[5:];
    currentBag.item_list["item"] = itemList;

    # saving this change 
    currentBag.save();

    print("the updated list of items is as follows \n", currentBag.item_list["item"]);
    print("The length after deletion of one item from the bag is as follows \n", len(currentBag.item_list["item"]));


    # say everything went fine 
    return currentBag;



# defining function to FastForward the delivery for the riders 
def fastForwardDelivery(listOfRiders):
    # using the for loop for this purpose 
    for rider in listOfRiders:
        currentRider = Rider.objects.get(email = rider);
        coordinates = currentRider.location_ids["coordinates"];
        coordinates = coordinates[5:];
        currentRider.location_ids["coordinates"] = coordinates;
        currentRider.save();

        # calling the function to also delete the list of items that are present in the riders bag 
        removeItemFromBag(currentRider);
    # say everything went fine 
    return;




# end point to fast forward the delivery location by 5 
class FastForward(APIView):
    # this will be a post request 
    def post(self, request):
        token = request.data["token"];
        randomNumber = request.data["randomNumber"];

        userName = Token.objects.get(key=token).user

        # we have to find the riders that were involved and then we have to delete the locations 
        # to simulate the fast forward thingy 
        listOfRiders = findListOfRidersInvolved(userName, randomNumber)

        # once we get the list of riders we have to delete the first 5 entries in their locations 
        # calling the function for this purpose 
        fastForwardDelivery(listOfRiders);

    
        # say everything went fine 
        return Response({"msg" : "success"}, status=status.HTTP_200_OK);



# function to find the remaining location and make excel sheet 
def findRemainingLocations(userName, randomNumber):
    # we have to find all the riders 
    listOfRiders = Rider.objects.filter(username = userName, random_number = randomNumber);
    print("the list of riders ++++++", listOfRiders)
    oldLocationsDictForMagicApi = [];
    RiderVsRemainingLocationsDict = {};
    listOfIds = []

    # using the for loop 
    for rider in listOfRiders:
        coordinates = rider.location_ids["coordinates"]
        RiderVsRemainingLocationsDict[rider.temp_id] = [];
        i = 0;
        tempDict = {}
        for point in coordinates:
            print(point);
            tempDict["id"] = point[0];
            tempDict["lat"] = point[1];
            tempDict["lng"] = point[2];
            tempArray = [point[1], point[2]];
            if(i != 0):
                RiderVsRemainingLocationsDict[rider.temp_id].append(point[0])
            listOfIds.append(point[0]);
            oldLocationsDictForMagicApi.append(tempDict.copy());
            # print("The oldloatiofsagsaklsjgksaj++++++++++++++++++++\n\n");
            # print(oldLocationsDictForMagicApi)
            i = i +1;

    # say everything went fine 
    return oldLocationsDictForMagicApi, listOfIds, RiderVsRemainingLocationsDict, listOfRiders;




# defining the function to convert the address to lat long 
def addressToLocations2(excelPath, userName, randomNumber, currentAlgoStatus):
    
    data = pd.read_excel(excelPath)
    places = data['address']
    # limit = 218
    data["lat"] =-1.00
    data["lng"] =-1.00

    for i in range(places.size):
        x =places[i]
        lat, lng, title , status= get_geocordinates(x)
        print(title)
        if lat==1000 or status==0:
            continue
        print()
        data['lat'][i]= lat
        data['lng'][i]= lng
        time.sleep(1)
        print(i," over")
    latLongCsvFilePath = "./data/" + str(currentAlgoStatus.dynamicPickUpExcelSheet)  + ".csv"
    print("The path of the geo_encoding with lat long coordinates is ", latLongCsvFilePath);
    data = data[(data["lat"]!=-1) & (data["lng"]!=-1)]
    # data.to_csv("./data/bangalore_dispatch_address_finals_out.csv")
    data.to_csv(latLongCsvFilePath);



# end point to add pick up points 
class DynamicPickUpPoints(APIView):
    # in this we have to upload the excel sheet for the dynamic pickup points 
    # this will be a post request 
    def post(self, request):
        print(request.data);
        print(request.FILES);
        data = request.data;
        token = data['token'];
        randomNumber = request.data["randomNumber"]
        file = request.FILES['file']


        excelData = pd.read_excel(file);


        #save the updated sheet
        excelData.to_excel(file)
        print("The content of the file is ", excelData);


        userName = Token.objects.get(key=token).user
        currentUser = PersonInfo.objects.get(email = str(userName))
        print('The token belongs to the following user\n\n', currentUser);
        userName = currentUser.email;
        

        currentAlgoStatus = AlgorithmStatusModel.objects.get(username = userName, random_number = randomNumber);
        currentAlgoStatus.dynamicPickUpExcelSheet = file;
        currentAlgoStatus.save();
        # time.sleep(10)
        addressToLocations2(str(file), userName, randomNumber, currentAlgoStatus)
        # step1 ==> store the remaining locations 
        latLongCsvFilePath = "./data/" + str(currentAlgoStatus.dynamicPickUpExcelSheet) + ".csv"
        print("the file path is as follows \n\n\n");
        print(latLongCsvFilePath)
        df = pd.read_csv(latLongCsvFilePath)
        lat = df["lat"]
        lng = df["lng"]
        print("The lat is ",(lat));
        print("The long is ",(lng));
        # df = pd.read_csv(latLongCsvFilePath)
        # lat = df["lat"]
        # lng = df["lng"]
        # print("The lat is ",type(lat));
        # print("The long is ",type(lng));
        # print("The type of item is ", type(i))
        if 'Volume' in df.columns:
            print("Volume column already exists")
        else:
            df['Volume'] = np.random.uniform(low=15000, high=40000, size=(len(df)))


        # we have to find the adjacency matrix using the think function and time matrix as well 
        distMatrixFileName = "./data/distance/distance_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
        print("distMatrixFileName ====== ", distMatrixFileName)
        timeMatrixFileName = "./data/time/time_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
        n = currentAlgoStatus.number_of_locations;
        distanceMatrix = think(distMatrixFileName, n).tolist();
        timeMatrix = think(timeMatrixFileName, n).tolist()  
        print(" distancematrix before====== ", distanceMatrix)

    # distance_matrix_war1@gmail.com_jquh71dq5b.csv
        # distanceMatrix=distanceMatrix.tolist();
        # print(" distancematrix after====== ", distanceMatrix)

        oldLocationsDictionaryForMagicApi, listOfIds, RiderVsRemainingLocationsDict, listOfRiders = findRemainingLocations(userName, randomNumber)
        currentLocation = Location.objects.get(username=userName, random_number = randomNumber);

        # we have to find the node weights 
        locationToItemWeight_nodeWeights = findNodeWeights(currentLocation)
        print("initial ridervslocationid", RiderVsRemainingLocationsDict)
        # print("The value of node weights is as follows \n\n\n", locationToItemWeight_nodeWeights);
        numberOfLocations = n;
        print("started\n\n\n\n");
        # using the for loop to find the distance for this purpose
        for i in range(0, 5):
            print("ball_status 1", i)
            new_pick_up = {"lat" : lat[i], "lng" : lng[i], "id" : n+i+1}
            # distanceArray, timeArray = api_call_pickup(new_pick_up, oldLocationsDictionaryForMagicApi);
            distanceArray, timeArray = api_call_pickup_dummy(new_pick_up, oldLocationsDictionaryForMagicApi);

            distanceArrayDict = {};
            k = 0;
            # now we have to make the distancedictionary to send the location_id vs distance 
            # using the for loop 
            for dist in distanceArray:
                distanceArrayDict[listOfIds[k]] = dist;
                k = k+1;
            
            # print("The distance array dictionary is as follows \n\n\n", distanceArrayDict);

            # similarly we have to calculate the time matrix 
            timeArrayDict = {};
            k = 0;
            for time in timeArray:
                timeArrayDict[listOfIds[k]] = time;
                k = k+1;
            
            # print("The time array dictionary is as follows \n\n\n", timeArrayDict);

            print("ball_status 2", i)


            # print("The distance matrix original thing is as follows \n\n", distanceMatrix)
            # print("The time matrix original thing is as follows \n\n", timeMatrix)

            # define the new node with [null, null, itemweight];
            # print("The item weight is ", df["Volume"][i]);
            newNode = [-1, -1, df["Volume"][i]]

            # we also need to create the new item in the database for this particular pickup point 
            random_string = "item" +  random_string_generator() ;
            newItem = Item.objects.create(item_name = random_string, item_volume = df["Volume"][i])
            # number of nodes same as before 
            

            # points will be passed as empty array for this purpose 
            points = [];

            # now we have to call the neels algorithm here 
            
            oriLocations = copy.deepcopy(RiderVsRemainingLocationsDict)
            print("oriLocations", oriLocations)
            numberOfDrivers = currentAlgoStatus.number_of_drivers
            print("nodes number of locations ", numberOfLocations);
            print("sisze of adjancet matrix  1 ", len(distanceMatrix));
            print("sisze of adjancet matrix 2 ", len(distanceMatrix[0]));


            # print("locationsResult", locationsResult)
            # print("totalCost", totalCost)
            # print("distanceMatrix", distanceMatrix)
            # print("timeMatrix", timeMatrix)
            # print("nodeWeights", nodeWeights)
            # print("m", m)


            print("numberOfDrivers", numberOfDrivers)
            print("RiderVsRemainingLocationsDict", RiderVsRemainingLocationsDict)
            print("locationToItemWeight_nodeWeights", locationToItemWeight_nodeWeights)
            print("distanceMatrix", distanceMatrix)
            print("timeMatrix", timeMatrix)
            print("numberOfLocations", numberOfLocations)
            print("newNode", newNode)
            print("distanceArrayDict", distanceArrayDict)
            print("timeArrayDict", timeArrayDict)
            print("points", points)


            # print("m", m)

            locationsResult, totalCost, distanceMatrix, timeMatrix, nodeWeights, m, points = pickup(numberOfDrivers, RiderVsRemainingLocationsDict, locationToItemWeight_nodeWeights, distanceMatrix, timeMatrix, numberOfLocations, newNode, distanceArrayDict, timeArrayDict, points)
            men = totalCost
            print("ball_status 3", i)

            ix = -1
            for neel_i in oriLocations:
                print("neel_i: ", neel_i, len(oriLocations[neel_i]), len(locationsResult[neel_i]))
                if(len(oriLocations[neel_i])+1 != len(locationsResult[neel_i])) : 
                    ix = neel_i
                    continue
                locationsResult[neel_i] = oriLocations[neel_i]
            # assert(ix != -1)
            print("ix valus is ", ix)
            if ( ix == -1):
                ix = random.randint(0,len(oriLocations)-1)
            print("ball_status 4", i)

            idx = -1
            try:
                idx = locationsResult.index(oriLocations[ix][0])
            except:
                myVeryPersonalVariable = None
                
            if (idx != -1):
                locationsResult[ix] = oriLocations[ix][idx:] + oriLocations[ix][1:idx]


            print("locationsResult is as follows+++++++++++ \n\n\n\n", locationsResult)

            # updaitn stuff 
            oldLocationsDictionaryForMagicApi.append(new_pick_up.copy())
            listOfIds.append(new_pick_up.copy()["id"])
            # for the nodeweight they already appended the stuff hence we will have to just update it 
            locationToItemWeight_nodeWeights = nodeWeights

            # we can also update the RiderVsRemainingLocationsDict 
            RiderVsRemainingLocationsDict = locationsResult;
            # updating the number of locations as it is auto incremented by the algorithm itself 
            numberOfLocations = m;
            print("OVERmessy", i);
            print(RiderVsRemainingLocationsDict)

    # once the algorithm finishes running then we will have to store the stuff in the database with 
    # the updated values of the rider pick up points and show to the frontend 
    # we have to store the new pickup locations in the location model along with their items 
    # store the updated ridervslocation_ids thing in the rider location section 
    # this can be done using the encoding that we have right now 
        return Response("done")

            


# end point to add pick up points 
class DummyDynamicPickUpPoints(APIView):
    # in this we have to upload the excel sheet for the dynamic pickup points 
    # this will be a post request 
    def post(self, request):
        print(request.data);
        print(request.FILES);
        data = request.data;
        token = data['token'];
        randomNumber = request.data["randomNumber"]
        file = request.FILES['file']


        excelData = pd.read_excel(file);


        #save the updated sheet
        excelData.to_excel(file)
        print("The content of the file is ", excelData);


        userName = Token.objects.get(key=token).user
        currentUser = PersonInfo.objects.get(email = str(userName))
        print('The token belongs to the following user\n\n', currentUser);
        userName = currentUser.email;
        

        currentAlgoStatus = AlgorithmStatusModel.objects.get(username = userName, random_number = randomNumber);
        currentAlgoStatus.dynamicPickUpExcelSheet = file;
        currentAlgoStatus.save();
        # time.sleep(10)
        # addressToLocations2(str(file), userName, randomNumber, currentAlgoStatus)
        # step1 ==> store the remaining locations 
        latLongCsvFilePath = "./data/" + str(currentAlgoStatus.dynamicPickUpExcelSheet) + ".csv"
        print("the file path is as follows \n\n\n");
        print(latLongCsvFilePath)
        df = pd.read_csv(latLongCsvFilePath)
        lat = df["lat"]
        lng = df["lng"]
        print("The lat is ",(lat));
        print("The long is ",(lng));
        # df = pd.read_csv(latLongCsvFilePath)
        # lat = df["lat"]
        # lng = df["lng"]
        # print("The lat is ",type(lat));
        # print("The long is ",type(lng));
        # print("The type of item is ", type(i))
        if 'Volume' in df.columns:
            print("Volume column already exists")
        else:
            df['Volume'] = np.random.uniform(low=15000, high=40000, size=(len(df)))


        # we have to find the adjacency matrix using the think function and time matrix as well 
        distMatrixFileName = "./data/distance/distance_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
        timeMatrixFileName = "./data/time/time_matrix_" + str(userName) + "_" + str(randomNumber) + ".csv";
        n = currentAlgoStatus.number_of_locations;
        distanceMatrix = think(distMatrixFileName, n).tolist();
        timeMatrix = think(timeMatrixFileName, n).tolist()  

        oldLocationsDictionaryForMagicApi, listOfIds, RiderVsRemainingLocationsDict, listOfRiders = findRemainingLocations(userName, randomNumber)
        currentLocation = Location.objects.get(username=userName, random_number = randomNumber);

        # we have to find the node weights 
        locationToItemWeight_nodeWeights = findNodeWeights(currentLocation)
        print("initial ridervslocationid", RiderVsRemainingLocationsDict)
        # print("The value of node weights is as follows \n\n\n", locationToItemWeight_nodeWeights);
        numberOfLocations = n;
        # using the for loop to find the distance for this purpose
        for i in range(0, 5):
            print("ball_status 1", i)
            new_pick_up = {"lat" : lat[i], "lng" : lng[i], "id" : n+i+1}
            # distanceArray, timeArray = api_call_pickup(new_pick_up, oldLocationsDictionaryForMagicApi);
            distanceArray, timeArray = api_call_pickup_dummy(new_pick_up, oldLocationsDictionaryForMagicApi);

            distanceArrayDict = {};
            k = 0;
            # now we have to make the distancedictionary to send the location_id vs distance 
            # using the for loop 
            for dist in distanceArray:
                distanceArrayDict[listOfIds[k]] = dist;
                k = k+1;
            
            # print("The distance array dictionary is as follows \n\n\n", distanceArrayDict);

            # similarly we have to calculate the time matrix 
            timeArrayDict = {};
            k = 0;
            for time in timeArray:
                timeArrayDict[listOfIds[k]] = time;
                k = k+1;
            
            # print("The time array dictionary is as follows \n\n\n", timeArrayDict);

            print("ball_status 2", i)


            # print("The distance matrix original thing is as follows \n\n", distanceMatrix)
            # print("The time matrix original thing is as follows \n\n", timeMatrix)

            # define the new node with [null, null, itemweight];
            # print("The item weight is ", df["Volume"][i]);
            newNode = [-1, -1, df["Volume"][i]]

            # we also need to create the new item in the database for this particular pickup point 
            random_string = "item" +  random_string_generator() ;
            newItem = Item.objects.create(item_name = random_string, item_volume = df["Volume"][i])
            # number of nodes same as before 
            

            # points will be passed as empty array for this purpose 
            points = [];

            # now we have to call the neels algorithm here 
            
            oriLocations = copy.deepcopy(RiderVsRemainingLocationsDict)
            print("oriLocations", oriLocations)
            numberOfDrivers = currentAlgoStatus.number_of_drivers
            print("nodes number of locations ", numberOfLocations);
            print("sisze of adjancet matrix  1 ", len(distanceMatrix));
            print("sisze of adjancet matrix 2 ", len(distanceMatrix[0]));


            # print("locationsResult", locationsResult)
            # print("totalCost", totalCost)
            # print("distanceMatrix", distanceMatrix)
            # print("timeMatrix", timeMatrix)
            # print("nodeWeights", nodeWeights)
            # print("m", m)


            print("numberOfDrivers", numberOfDrivers)
            print("RiderVsRemainingLocationsDict", RiderVsRemainingLocationsDict)
            print("locationToItemWeight_nodeWeights", locationToItemWeight_nodeWeights)
            print("distanceMatrix", distanceMatrix)
            print("timeMatrix", timeMatrix)
            print("numberOfLocations", numberOfLocations)
            print("newNode", newNode)
            print("distanceArrayDict", distanceArrayDict)
            print("timeArrayDict", timeArrayDict)
            print("points", points)


            # print("m", m)

            locationsResult, totalCost, distanceMatrix, timeMatrix, nodeWeights, m, points = pickup(numberOfDrivers, RiderVsRemainingLocationsDict, locationToItemWeight_nodeWeights, distanceMatrix, timeMatrix, numberOfLocations, newNode, distanceArrayDict, timeArrayDict, points)
            men = totalCost
            print("ball_status 3", i)

            ix = -1
            for neel_i in oriLocations:
                print("neel_i: ", neel_i, len(oriLocations[neel_i]), len(locationsResult[neel_i]))
                if(len(oriLocations[neel_i])+1 != len(locationsResult[neel_i])) : 
                    ix = neel_i
                    continue
                locationsResult[neel_i] = oriLocations[neel_i]
            # assert(ix != -1)
            print("ix valus is ", ix)
            if ( ix == -1):
                ix = random.randint(0,len(oriLocations)-1)
            print("ball_status 4", i)

            idx = -1
            try:
                idx = locationsResult.index(oriLocations[ix][0])
            except:
                myVeryPersonalVariable = None
                
            if (idx != -1):
                locationsResult[ix] = oriLocations[ix][idx:] + oriLocations[ix][1:idx]


            print("locationsResult is as follows+++++++++++ \n\n\n\n", locationsResult)

            # updaitn stuff 
            oldLocationsDictionaryForMagicApi.append(new_pick_up.copy())
            listOfIds.append(new_pick_up.copy()["id"])
            # for the nodeweight they already appended the stuff hence we will have to just update it 
            locationToItemWeight_nodeWeights = nodeWeights

            # we can also update the RiderVsRemainingLocationsDict 
            RiderVsRemainingLocationsDict = locationsResult;
            # updating the number of locations as it is auto incremented by the algorithm itself 
            numberOfLocations = m;
            print("OVERmessy", i);
            print(RiderVsRemainingLocationsDict)

    # once the algorithm finishes running then we will have to store the stuff in the database with 
    # the updated values of the rider pick up points and show to the frontend 
    # we have to store the new pickup locations in the location model along with their items 
    # store the updated ridervslocation_ids thing in the rider location section 
    # this can be done using the encoding that we have right now 

            






        # print()
        # # step2 ==> give this to magic api and it will return the distance and time matrix 
        # distance = [];
        # time = [];

        # # step 3 ==> make the dictionary with location_id : distance 
        # distanceDictionary = {};
        # timeDictionary = {};
        # i = 0;
        # for ele in distance:
        #     distanceDictionary[listOfIds[i]] = ele;
        #     i = i+1;
        
        # i = 0;
        # for ele in time:
        #     timeDictionary[listOfIds[i]] = ele;
        #     i = i+1;
        

        # here we have to call the neels algo and store the results 

        # calculate the distance 
        # say everything went fine 
        return Response({"msg" : "success", "data" : "Uploaded the Dynamic Pickup Points"}, status=status.HTTP_200_OK);


class CvPoint(APIView):
    def post(self, request):
        file1 = request.FILES["file1"];
        # file2 = request.FILES["file2"];
        print("the file 1 is ", file1);
        
        # print("the file 2
        #  is ", file2);
        return Response("1");