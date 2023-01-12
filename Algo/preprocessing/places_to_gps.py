
## kindly run this inside the pre preocessing 

import pandas as pd
import requests
import time 

def get_geocordinates(place):

    place= place.replace(" ", "+ ")
    url = "https://discover.search.hereapi.com/v1/discover?at=12.7307999,77.9973085&limit=2&q="+place+"&apiKey=6QNNTzC1zysibIBzUnTnBAg5KY1Qc4BBEBElSnrMvSo"

    response = requests.get(url)

    if response.status_code == 200:    # Check if request was successful
        data = response.json()         # Get JSON result
        title = data['items'][0]['title']
        geo = data['items'][0]['position']
        lat = geo['lat']
        lng = geo['lng']
            # print("title: ", title)
            # print("lat: ", lat)
            # print("lng: ", lng)

        return lat, lng, title
    return 1000, 1000, "NIL" 

print("Start")

# data = pd.read_excel('../dataset/bangalore_dispatch_address_finals.xlsx')
data = pd.read_excel('../dataset/bangalore_pickups.xlsx')
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

data.to_csv("bangalore_pickups_out.csv")

print("over")

