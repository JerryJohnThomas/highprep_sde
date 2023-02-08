
import csv 

# defining the function to find the total number of locations 
def findNumberOfLocations(latLongCsvFilePath):

    with open(latLongCsvFilePath, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    total_entries = len(data)
    # print("The total number of locations are as follows +++++\n\n", totale)
    # print(total_entries-1)

    # say everything went fine 
    return total_entries;




findNumberOfLocations("../data/war1@gmail.com_t5abgwkjun.csv")