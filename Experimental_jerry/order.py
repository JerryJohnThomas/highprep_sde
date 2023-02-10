import pandas as pd

data = pd.read_excel("./bangalore dispatch address.xlsx")
def add_front_zero(temp):
    splitted = temp.split("-")
    date, month, year= splitted[0], splitted[1], splitted[2]
    if(len(date)==1):
        date="0"+date
    new_date = date+"-"+month+"-"+year
    return new_date

data['EDD'] = data['EDD'].apply(lambda x: add_front_zero(x))
data = data.sort_values(by='EDD', ascending=True)
