import numpy as np
import pandas as pd
import requests
import time
import datetime as dt

# function to get the distance time matrix 
def calculateDistanceTimeMatrix_OSRM(filePath):
    
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

    max_size_count = 25
    for i in range(0,size,max_size_count):
        batches.append(places[i:min(i+max_size_count,size)])


    arr = np.arange(0,size) 
    dist_mat = pd.DataFrame( index=arr, columns=arr)
    time_mat = pd.DataFrame( index=arr, columns=arr)


    print("total batches ", len(batches))

    for id_i,data_i in enumerate(batches):
        id_range_i = np.arange(id_i*max_size_count, id_i*max_size_count + len(data_i))
        
        for id_j,data_j in enumerate(batches):
            id_range_j = np.arange(id_j*max_size_count, id_j*max_size_count + len(data_j))
            
            # print(id_range_i," XX ",id_range_j)
            dist_batch, time_batch = api_call_osrm(data_i,data_j)
            # updaing the csv
            for j in id_range_j:
                for i in id_range_i:
                    # print("accessing indices", i-id_range_i[0])
                    key_i = i-id_range_i[0]
                    key_j = j-id_range_j[0]
                    # i changed str(j) to int(j)
                    dist_mat.at[int(i),int(j)] = dist_batch[key_i][key_j]
                    time_mat.at[int(i),int(j)] = time_batch[key_i][key_j]
            print(id_i," and ",id_j," is over")

    time_now = dt.now().isoformat()
    time_now= time_now.replace(":",".")

    write_csv=True
    distMatrixFileName = "distance_matrix_" + ".csv"
    timeMatrixFileName = "time_matrix_" + ".csv"
    if write_csv:
        dist_mat.to_csv(f"./{distMatrixFileName}", index=True)
        time_mat.to_csv(f"./{timeMatrixFileName}", index=True)

def calculate_distance2(ss):
    url = 'http://router.project-osrm.org/table/v1/driving/'+ss
    response = requests.get(url)
    data = response.json()
    distance = data['durations']
    return distance


def api_call_osrm(origins, destinations):
    # origins is an array where each item is an aarray [index, latitiude ,longitide]
    size1 = len(origins)
    size2 = len(destinations)
    

    full_str = ""
    for places in range(origins):
        places = str(places[2])+","+str(places[1])
        full_str = full_str+places+";"
    for places in range(destinations):
        places = str(places[2])+","+str(places[1])
        full_str = full_str+places+";"
    full_str = full_str[:-1]

    ss = "sources="
    for i in range(len(origins)):
        ss=ss+str(i+1)+";"
    ss = ss[:-1]

    full_str= full_str+"?"+ss
    distance = calculate_distance2(full_str)
    return distance

