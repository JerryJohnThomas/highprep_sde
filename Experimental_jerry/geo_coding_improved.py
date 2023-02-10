
# ## kindly run this inside the pre preocessing 

# import pandas as pd
# import requests
# import time 

# def get_geocordinates(place):

#     place= place.replace(" ", "+ ")
#     url = "https://discover.search.hereapi.com/v1/discover?at=12.7307999,77.9973085&limit=2&q="+place+"&apiKey=6QNNTzC1zysibIBzUnTnBAg5KY1Qc4BBEBElSnrMvSo"

#     response = requests.get(url)

#     if response.status_code == 200:    # Check if request was successful
#         data = response.json()         # Get JSON result
#         title = data['items'][0]['title']
#         geo = data['items'][0]['position']
#         lat = geo['lat']
#         lng = geo['lng']
#         print("title: ", title)
#         print("lat: ", lat)
#         print("lng: ", lng)

#         return lat, lng, title

# print("Start")

# data = pd.read_excel('../dataset/bangalore_dispatch_address_finals.xlsx')
# places = data['address']
# limit =2
# data["lat"] =-1
# data["lng"] =-1

# for i in range(limit):
#     x =places[i]
#     print(x)
#     lat, lng, title = get_geocordinates(x)
#     print()
#     data[lat][i]= lat
#     data[lng][i]= lng
#     time.sleep(1)



# print("over")

import requests
import numpy as np
import json

def api_call(origins, destinations):
    # origins is an array where each item is an aarray [index, latitiude ,longitide]
    size1 = len(origins)
    size2 = len(destinations)
    
    distance_res = np.zeros([size1,size2])
    time_res = np.zeros([size1,size2])

    body = { "origins": [],
        'apiKey': 'HERE-f3ed6874-fecb-4448-86ff-371411176981',
        'app_id' : 'SDdtuyFAQvF2SPkmY0xJ',
        # 'app_code': ,
    # 'app_code': token,
    #  "destinations" : [],
      "travelMode": "DRIVE",
        "regionDefinition": {
        "type": "circle",
        "center": {"lat": 12.91, "lng": 77.57},
        "radius": 10000
    }
    #   "routingPreference": "TRAFFIC_AWARE"        ## uncommenting this will make the api higher priced and can do a max of 10 points as opposed to 25 points in a singel call
    }

        # body['origins'].append({"waypoint": {"location": {"latLng": {"latitude": location[1], "longitude": location[2]}}}})
    for location in origins:
        body['origins'].append({"lat": location[1], "lng": location[2]})
    
    # for location in destinations:
    #     body['destinations'].append({"waypoint": {"location": {"latLng": {"latitude": location[1], "longitude": location[2]}}}})

    # print(body)

#     POST https://matrix.router.hereapi.com/v8/matrix?async=false
# Content-Type: application/json
# Body:
# {
#     "origins": [{"lat": 0.0, "lng": 0.0}, {"lat": 0.1, "lng": 0.1}, ...],
#     "destinations": [...],  // if omitted same as origins
#     "regionDefinition": {
#         "type": "circle",
#         "center": {"lat": 0.0, "lng": 0.0},
#         "radius": 10000
#     }
# }


    headers = {
        'Content-Type': 'application/json',
        # 'X-Goog-Api-Key': 'AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g',
        # 'X-Goog-FieldMask': 'originIndex,destinationIndex,duration,distanceMeters,status,condition',
    }

    # call = requests.post('https://matrix.router.hereapi.com/v8/matrix?async=false', json=body, headers=headers)
    call = requests.post('https://matrix.route.api.here.com/routing/7.2/calculatematrix.json', json=body, headers=headers)
    res = call.text

    print(call.status_code, call.reason)
    print(call.text)
    json_object = json.loads(call.text)

    # print(len(json_object))
    # for id,data in enumerate(json_object):
    #     # print(id, data)
    #     ind1 = data["originIndex"]
    #     ind2 = data["destinationIndex"]
    #     time = int(data["duration"][:-1])
        
    #     if ind1 == ind2 or time==0:
    #         dist = 0
    #     else:
    #         dist = data["distanceMeters"]

    #     distance_res[ind1][ind2] = dist
    #     time_res[ind1][ind2] = time

    return distance_res , time_res

origins = [[0, 12.91345, 77.57498], [1, 12.94022, 77.53995]]
dest = [[50, 12.89963, 77.64903], [51, 12.9319, 77.60736]]


api_call(origins,dest)