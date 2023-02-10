import requests
import pandas as pd
import math
import numpy as np

data = pd.read_csv("./test1.csv")
lat, lng = data['lat'], data['lng']

size = min(len(lat), 10)

def calculate_distance(start_coord, end_coord):
    url = 'http://router.project-osrm.org/route/v1/driving/{0};{1}?overview=false'.format(start_coord, end_coord)
    print(url)
    response = requests.get(url)
    data = response.json()
    distance = data['routes'][0]['distance']
    return distance

def calculate_distance2(ss):
    url = 'http://router.project-osrm.org/table/v1/driving/'+ss
    print("//")
    print(url)
    print("//")
    response = requests.get(url)
    data = response.json()
    distance = data['durations']
    # distance = data['destinations'][0]['distance']
    return distance

start_coord = '13.388860,52.517037'
end_coord = '13.428555,52.523219'
distance = calculate_distance(start_coord, end_coord)

# print(distance)


def cal_matrix(lat,lng):

    matrix = np.zeros([size,size])
    print(matrix)
    full_str = ""
    for i in range(size):
        place_i = str(lat[i])+","+str(lng[i])
        full_str = full_str+place_i+";"
    full_str = full_str[:-1]
    print(full_str)
    distance = calculate_distance2(full_str)
    return distance


ans = cal_matrix(lat,lng)
print("************************")
print(ans)

