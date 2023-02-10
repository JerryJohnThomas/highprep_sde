import pandas as pd



data = pd.read_excel("./bangalore dispatch address.xlsx")

## ordering section
def add_front_zero(temp):
    splitted = temp.split("-")
    date, month, year= splitted[0], splitted[1], splitted[2]
    if(len(date)==1):
        date="0"+date
    new_date = date+"-"+month+"-"+year
    return new_date


# add both the lines together to sort it
data['EDD'] = data['EDD'].apply(lambda x: add_front_zero(x))
data = data.sort_values(by='EDD', ascending=True)


## next section


# we have to do min(n*23, remaining points)

# start index
start = 0 
n =2
block_size = n*23
len = len(data)
print("len: ",len)
# print(len)
# # end index 
end = min(start+block_size, len)
day_count = 0

while end <= len:
    print(start, end, " on day: ",day_count)
    # you can do data[start:end]
    start=end
    end = min(start+block_size, len)
    day_count= day_count+1
    if start==end:
        break

    
