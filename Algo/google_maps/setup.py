import pandas as pd 
import numpy as np

size=218
arr = np.arange(0,size) 
df = pd.DataFrame( index=arr, columns=arr)
df.to_csv("distance_matrix_"+str(size)+".csv")
print("directions matrix created of size", size)
df.to_csv("time_matrix_"+str(size)+".csv")
print("Time created of size", size)

# arr = np.arange(0,2) 
# df = pd.DataFrame([[10,20],[30,40]], index=arr, columns=arr)
# df[1][1]=75


