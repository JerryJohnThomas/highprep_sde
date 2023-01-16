import pandas as pd 
import requests
import json
# from dotenv import load_dotenv
# config = dotenv_values("sarthak.env")



df = pd.read_csv("../preprocessing/bangalore_dispatch_address_finals_out.csv")
lat = df["lat"]
lng = df["lng"]

print(lat.size)

def api_call():
    print("starting api call")
    body= {
        "origins": [
    {
        "waypoint": {
        "location": {
            "latLng": {
            "latitude": 37.420761,
            "longitude": -122.081356
            }
        }
        },
    },
    {
        "waypoint": {
        "location": {
            "latLng": {
            "latitude": 37.403184,
            "longitude": -122.097371
            }
        }
        },
    }
    ],
    "destinations": [
    {
        "waypoint": {
        "location": {
            "latLng": {
            "latitude": 37.420999,
            "longitude": -122.086894
            }
        }
        }
    },
    {
        "waypoint": {
        "location": {
            "latLng": {
            "latitude": 37.383047,
            "longitude": -122.044651
            }
        }
        }
    }
    ],
    "travelMode": "DRIVE",
    #   "routingPreference": "TRAFFIC_AWARE"
    }

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': 'AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g',
        'X-Goog-FieldMask': 'originIndex,destinationIndex,duration,distanceMeters,status,condition',
    }
    # 'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    # 'Authorization': '5b3ce3597851110001cf6248b76e3c4096b7467c86421b2f6b8bdef2',
    # 'Content-Type': 'application/json; charset=utf-8'

    call = requests.post('https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix', json=body, headers=headers)

    print(call.status_code, call.reason)
    # print(call.text)
    # print()

    json_object = json.loads(call.text)
    print(json.dumps(json_object, indent=4))


api_call()

