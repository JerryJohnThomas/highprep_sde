import threading
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

from .serializers import AlgorithmStatusModelSerializer,RiderSerializer
from .models import AlgorithmStatusModel, Location, Rider
from login_apis.models import PersonInfo
from rider_apis.models import Bag
from inventory_apis.models import Item
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
        if lat==1000 or status==0:
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

        # latitude = [];
        # longitude = [];
        coordinates = [];
        random_string = "item" +  random_string_generator() ;
        # here we will have to create the new item in the database as we are getting it from excel sheet 
        newItem = Item.objects.create(item_name = random_string, item_volumne = df["item"][i])
        # using the for loop for this purpose 
        for i in range(lat.size):
            coordinates.append([i+1, df['lat'][i], df['lng'][i], newItem.item_name])


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
        currentRider.temp_id = i+1;
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








# defining the function to find the total number of locations 
def findNumberOfLocations(currentAlgorithm, latLongCsvFilePath):

    with open(latLongCsvFilePath, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    total_entries = len(data)

    print(total_entries)

    # say everything went fine 
    return total_entries-2;






# function to find the map of location_id and item weight 
def findNodeWeights(currentLocation):
    coordinates = currentLocation.location_array["coordinates"];

    itemVolumeNodeWeights = {};

    # using the for loop for this purpose 
    for entry in coordinates:
        itemName = entry[3];
        itemVolume = Item.objects.get(item_name = itemName).item_volume
        itemVolumeNodeWeights[entry[0]] = itemVolume;


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
        markThemAsNonAvailable(availableNRiders);

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
        totalLocations = findNumberOfLocations(currentAlgorithm, latLongCsvFilePath);
        currentAlgorithm.number_of_locations = totalLocations;
        currentAlgorithm.save();

        # creating the dictionary for item weights 
        locationToItemVolume_nodeWeights = findNodeWeights(currentLocation);

        deliveryManBagWeight = findBagWeightsOfRiders(availableNRiders);
        
        # timeMatrixFileName = "./time_matrix218_2023-01-21T17.04.47.497441.csv"
        # now i will be calling the NEEL's algo here 
        algoRes = think(timeMatrixFileName, n)

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
            currentLatLong = coordinates[key-1];
            riderIdVsLoc[algoRes[key]-1].append(currentLatLong);
        

        print("The final mapping of riderid vs loc is as follows \n\n");
        print(riderIdVsLoc)

        riderLocationDict = storeLocationsInRiderCollection(currentUser.email, randomNumber, riderIdVsLoc, availableNRiders);

        # now we also have to create new bag for each of this riders 
        createBagForEachRiders(availableNRiders);







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
    
    oldLocationsDictForMagicApi = [];
    RiderVsRemainingLocationsDict = {};
    listOfIds = []

    # using the for loop 
    for rider in listOfRiders:
        coordinates = rider.location_ids["coordinates"]
        RiderVsRemainingLocationsDict[rider.temp_id] = [];

        tempDict = {}
        for point in coordinates:
            tempDict["id"] = point[0];
            tempDict["lat"] = point[1];
            tempDict["lng"] = point[2];
            tempArray = [point[1], point[2]];
            RiderVsRemainingLocationsDict[rider.temp_id].append(tempArray)
            listOfIds.append(point[0]);
            oldLocationsDictForMagicApi.append(tempDict);

    # say everything went fine 
    return oldLocationsDictForMagicApi, listOfIds, RiderVsRemainingLocationsDict;



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

   
        # step1 ==> store the remaining locations 
        oldLocationsDictionaryForMagicApi, listOfIds, RiderVsRemainingLocationsDict = findRemainingLocations(userName, randomNumber)
        
        # step2 ==> give this to magic api and it will return the distance and time matrix 
        distance = [];
        time = [];

        # step 3 ==> make the dictionary with location_id : distance 
        distanceDictionary = {};
        timeDictionary = {};
        i = 0;
        for ele in distance:
            distanceDictionary[listOfIds[i]] = ele;
            i = i+1;
        
        i = 0;
        for ele in time:
            timeDictionary[listOfIds[i]] = ele;
            i = i+1;
        

            # timeDictionary[listOfIds[i]] = 

        storeLatLongInDb()

        # calculate the distance 
        # say everything went fine 
        return Response({"msg" : "success", "data" : "Uploaded the Dynamic Pickup Points"}, status=status.HTTP_200_OK);
        