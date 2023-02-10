import numpy as np
import pandas as pd

print("started")
data = pd.read_excel('./bangalore dispatch address.xlsx')
ad = data['address']

clusters ={}

for i in range(len(ad)):
    temp = ad.iloc[i]
    # print(i,"  ",temp)
    if (len(temp)<=2 or (',' in temp)==False):
        continue
        cluster_name=temp.split(",")[-1]
    else:
        cluster_name=temp.split(",")[-2]
    cluster_name = cluster_name.strip()
    if cluster_name not in clusters:
        clusters[cluster_name] = 0 
    clusters[cluster_name] = clusters[cluster_name] + 1 


counter=0
for key in clusters:
    if clusters[key]>=10:
        counter=counter+1

print(clusters)
print(len(clusters))
print(counter)
print("over")


