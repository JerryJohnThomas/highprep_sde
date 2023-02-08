import numpy as np
import json
import requests
from numpy import random 

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

origins = [[0, 12.91345, 77.57498], [1, 12.94022, 77.53995], [2, 12.91275, 77.58582], [3, 12.94022, 77.53995], [4, 12.90662, 77.59663], [5, 12.86796, 77.58457], [6, 12.90826, 77.61137], [7, 12.90206, 77.58585], [8, 12.89096, 77.5834], [9, 12.98276, 77.60712], [10, 12.90012, 77.59566], [11, 12.89986, 77.58587], [12, 12.91054, 77.59913], [13, 12.90641, 77.59292], [14, 12.90756, 77.59837], [15, 12.90445, 77.59639], [16, 12.90611, 77.59661], [17, 12.88876, 77.58247], [18, 12.8964, 77.58617], [19, 12.89986, 77.58587], [20, 12.87544, 77.58334], [21, 12.88557, 77.58231], [22, 12.90654, 77.59849], [23, 12.89838, 77.59681], [24, 12.90258, 77.59664]]
dest = [[50, 12.89963, 77.64903], [51, 12.9319, 77.60736], [52, 12.91586, 77.64479], [53, 12.91966, 77.65186], [54, 12.91199, 77.6518], [55, 12.9121, 77.64958], [56, 12.89757, 77.65878], [57, 12.9366, 77.6148], [58, 12.91248, 77.65201], [59, 12.91232, 77.65167], [60, 12.91576, 77.64931], [61, 12.91586, 77.64479], [62, 12.91248, 77.65201], [63, 12.91951, 77.64992], [64, 12.91575, 77.64901], [65, 12.91967, 77.65105], [66, 12.91595, 77.64929], [67, 12.91279, 77.6536], [68, 12.91967, 77.65105], [69, 12.91182, 77.64814], [70, 12.91529, 77.64891], [71, 12.92212, 77.65145], [72, 12.91571, 77.65253], [73, 12.91571, 77.65253], [74, 12.9215, 77.65155]]

origins3 = [[0, 12.91345, 77.57498], [1, 12.94022, 77.53995], [2, 12.91275, 77.58582]]
dest3 = [[50, 12.89963, 77.64903], [51, 12.9319, 77.60736], [52, 12.91586, 77.64479]]

# api_call(origins, dest)
# api_call(origins3, dest3)

# def api_call(a,b):
#     return api_call_dummy(a,b)
    
#  this is magic api @rupesh
def api_call_pickup(new_point, list_old_pts):
    size = len(list_old_pts)
    distance_res = np.zeros([size])
    time_res = np.zeros([size])

    body = { "origins": [], "destinations" : [], "travelMode": "DRIVE",
    #   "routingPreference": "TRAFFIC_AWARE"        ## uncommenting this will make the api higher priced and can do a max of 10 points as opposed to 25 points in a singel call
    }
    print("jj: origin" ,new_point)
    print("jj: dest" ,list_old_pts)

    for location in [new_point]:
        body['origins'].append({"waypoint": {"location": {"latLng": {"latitude": location["lat"], "longitude": location["lng"]}}}})
    
    for location in list_old_pts:
        body['destinations'].append({"waypoint": {"location": {"latLng": {"latitude": location["lat"], "longitude": location["lng"]}}}})

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
        ind2 = data["destinationIndex"]
        time = int(data["duration"][:-1])
        
        if time==0:
            dist = 0
        else:
            dist = data["distanceMeters"]

        distance_res[ind2] = dist
        time_res[ind2] = time

    return distance_res , time_res



def api_call_pickup_dummy(new_point, list_old_pts):
    size = len(list_old_pts)
    distance_res = np.random.randint(0, 100, size)
    time_res = np.random.randint(0, 100, size)
    print("distance res ", distance_res)
    print("time res ", time_res)
    return distance_res , time_res
