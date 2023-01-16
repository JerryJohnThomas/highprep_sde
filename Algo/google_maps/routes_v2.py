import pandas as pd 
import requests
import json
import numpy as np
from maps_route_api import api_call
import time
from datetime import datetime as dt
import time

df = pd.read_csv("../preprocessing/bangalore_dispatch_address_finals_out.csv")
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
for i in range(0,size,25):
    batches.append(places[i:min(i+25,size)])


# # batch data display
# for id,data in enumerate(batches):
#     print("batch:", id, "range: [", id*25,",",id*25+len(data),"]")
#     print(data)
#     print("---------------------------")


dist_mat = pd.read_csv("./distance_matrix_218.csv")
time_mat = pd.read_csv("./time_matrix_218.csv")

print("total batches ", len(batches))

for id_i,data_i in enumerate(batches):
    id_range_i = np.arange(id_i*25, id_i*25 + len(data_i))
    
    for id_j,data_j in enumerate(batches):
        id_range_j = np.arange(id_j*25, id_j*25 + len(data_j))
        
        # print(id_range_i," XX ",id_range_j)
        dist_batch, time_batch = api_call(data_i,data_j)
        # updaing the csv
        for j in id_range_j:
            for i in id_range_i:
                # print("accessing indices", i-id_range_i[0])
                key_i = i-id_range_i[0]
                key_j = j-id_range_j[0]
                dist_mat.at[int(i),str(j)] = dist_batch[key_i][key_j]
                time_mat.at[int(i),str(j)] = time_batch[key_i][key_j]
        time.sleep(15)
        print(id_i," and ",id_j," is over")

time_now = dt.now().isoformat()
time_now= time_now.replace(":",".")

write_csv=True

if write_csv:
    dist_mat.to_csv("distance_matrix"+str(size)+"_"+time_now+".csv", index=False)
    dist_mat.to_csv("time_matrix"+str(size)+"_"+time_now+".csv", index=False)






