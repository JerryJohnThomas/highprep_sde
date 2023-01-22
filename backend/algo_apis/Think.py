# read the csv shhet
# make it 1 indexed 
# replace 0's with infity 


# pass to neels 

import pandas as pd
import numpy as np
from .Neel import solve 

# time_matrix218_2023-01-21T17.04.47.497441
def think(time_filename):
    time = pd.read_csv(time_filename)
    # print(time)

    num_rows, num_cols = time.shape
    np_matrix = np.array(time)

    np_matrix = np.column_stack((np.zeros(num_rows), np_matrix ))
    np_matrix = np.append([np.zeros(num_cols+1)], np_matrix, axis=0 )
    np_matrix[np_matrix == 0] = np.inf 

    res = solve(219,5,np_matrix)
    print("\n\n\n\n")
    print(res)
    return res;


