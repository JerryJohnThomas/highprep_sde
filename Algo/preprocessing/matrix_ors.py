import requests
import json
# https://openrouteservice.org/dev/#/api-docs/v2/matrix/{profile}/post

# body = {"locations":[[9.70093,48.477473],[9.207916,49.153868],[37.573242,55.801281],[115.663757,38.106467]]}
# this was provied as sample this is working


# the below are obtained from the dataset, its working on google maps manually but in this api call
# body = {"locations":[[12.91345,77.57498],[12.89757,77.65878],[12.91182,77.64814],[12.9169,77.65171]]}
body = {"locations":[[12.91345,77.57498],[12.89757,77.65878]]}

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf6248b76e3c4096b7467c86421b2f6b8bdef2',
    'Content-Type': 'application/json; charset=utf-8'
}
call = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers)

print(call.status_code, call.reason)
print(call.text)
print()

json_object = json.loads(call.text)
print(json.dumps(json_object, indent=4))