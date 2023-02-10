import requests
import pandas as pd
import math
import numpy as np

data = pd.read_csv("./test1.csv")
lat, lng = data['lat'], data['lng']

size = min(len(lat), 10)

def calculate_distance(start_coord, end_coord):
    url = 'http://router.project-osrm.org/route/v1/driving/{0};{1}?overview=false'.format(start_coord, end_coord)
    response = requests.get(url)
    data = response.json()
    distance = data['routes'][0]['distance']
    return distance

def calculate_distance2(ss):
    url = 'http://router.project-osrm.org/route/v1/driving/'+ss
    response = requests.get(url)
    data = response.json()
    print(data)
    temp = data['routes'][0]["legs"][0]
    print(temp)
    print(len(temp))
    distance= []
    for i in range(len(temp)):
        print(temp[i])
        temp_dis = temp[i]["distance"]
        print(temp_dis)
        if i%2==0:
            distance.append(temp_dis)
        else:
            continue
    return distance

start_coord = '13.388860,52.517037'
end_coord = '13.428555,52.523219'
distance = calculate_distance(start_coord, end_coord)

# print(distance)


# matrix = np.zeros([size,size])
# print(matrix)
# full_str = ""
# for i in range(size):
#     place_i = str(lat[i])+","+str(lng[i])
#     full_str = full_str+place_i+";"
#     for j in range(size):
#         place_j = str(lat[j])+","+str(lng[j])
#         full_str = full_str+place_j+";"
#         full_str = full_str+place_i+";"
#     full_str = full_str[:-1]
#     distance = calculate_distance2(full_str)[0]
#     matrix[i][j]=distance
#     print(i,"  ",j,"over")

matrix = np.zeros([size,size])
print(matrix)
full_str = ""
for i in range(size):
    place_i = str(lat[i])+","+str(lng[i])
    full_str = full_str+place_i+";"
    for j in range(size):
        place_j = str(lat[j])+","+str(lng[j])
        full_str = full_str+place_j+";"
        full_str = full_str+place_i+";"
    full_str = full_str[:-1]
    distance = calculate_distance2(full_str)[0]
    matrix[i][j]=distance
    print(i,"  ",j,"over")

print(matrix)

