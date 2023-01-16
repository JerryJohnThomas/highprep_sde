import pandas as pd 
import requests
import json
import numpy as np
from maps_route_api import api_call
import time
from datetime import datetime as dt

df = pd.read_csv("../preprocessing/bangalore_dispatch_address_finals_out.csv")
lat = df["lat"]
lng = df["lng"]

dist_mat = pd.read_csv("./distance_matrix_218.csv")
time_mat = pd.read_csv("./time_matrix_218.csv")


# print(dist_mat[0][0])
print(dist_mat.size)
print(dist_mat.shape)
print(dist_mat.iloc[0][0])
print(dist_mat.iloc[0][1])
dist_mat.at['0','0'] = 12
print(dist_mat.iloc[0][0])
print(dist_mat.iloc[0][1])

for i in range(10):
    dist_mat.at[1,str(i)] = i+20

for i in range(10):
    dist_mat.at[i,'0'] = i+30
    dist_mat.at[i,'1'] = i+40

dist_mat.to_csv("./test1.csv")
# print(dist_mat[0,0])

