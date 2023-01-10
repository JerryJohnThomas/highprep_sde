
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
        print("title: ", title)
        print("lat: ", lat)
        print("lng: ", lng)

        return lat, lng, title

print("Start")

data = pd.read_excel('../dataset/bangalore_dispatch_address_finals.xlsx')
places = data['address']
limit =2
data["lat"] =-1
data["lng"] =-1

for i in range(limit):
    x =places[i]
    print(x)
    lat, lng, title = get_geocordinates(x)
    print()
    data[lat][i]= lat
    data[lng][i]= lng
    time.sleep(1)



print("over")

