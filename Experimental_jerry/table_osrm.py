import requests
import pandas as pd
import math
import numpy as np

data = pd.read_csv("./test2.csv")
lat, lng = data['lat'], data['lng']


def calculate_distance(start_coord, end_coord):
    url = 'http://router.project-osrm.org/route/v1/driving/{0};{1}?overview=false'.format(start_coord, end_coord)
    response = requests.get(url)
    data = response.json()
    distance = data['routes'][0]['distance']
    return distance

def calculate_distance2(ss):
    url = 'http://router.project-osrm.org/table/v1/driving/'+ss
    # print("//")
    # print(url)
    # print("//")
    response = requests.get(url)
    data = response.json()
    distance = data['durations']
    # distance = data['destinations'][0]['distance']
    return distance

start_coord = '13.388860,52.517037'
end_coord = '13.428555,52.523219'
distance = calculate_distance(start_coord, end_coord)

# print(distance)

print(len(lat))
def cal_matrix(lat,lng):

    size = min(len(lat), 100)
    # size = len(lat)
    matrix = np.zeros([size,size])
    full_str = ""
    for i in range(size):
        # place_i = str(lat[i])+","+str(lng[i])
        place_i = str(lng[i])+","+str(lat[i])
        full_str = full_str+place_i+";"
    full_str = full_str[:-1]
    distance = calculate_distance2(full_str)
    return distance



for i in range(25):
    ans = cal_matrix(lat,lng)
    print("************************", "   ",i)
print(ans)

