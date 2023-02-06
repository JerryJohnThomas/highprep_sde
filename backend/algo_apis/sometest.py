import csv

with open('./data/pandey5@gmail.com_gutatlpv1o.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

total_entries = len(data)

print(total_entries)