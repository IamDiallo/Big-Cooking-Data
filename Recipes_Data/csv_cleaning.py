import pandas as pd
import numpy as np
import json
import csv

data = pd.read_csv("test.csv", encoding='UTF-8')
data.rename(columns={"difficylty":"difficulty"})
print(data.columns)
#print(data.head())
data.columns = data.columns.str.upper()
#print(data.columns)

data.rename(columns={"DIFFICULTY":"DIFFICYLTY"})
print(data.columns)
#print(data.isnull().sum())
#print(data.shape)

data_drop = data.dropna()
#print(data_drop.isnull().sum())
#print(data_drop['ETAPE'])
#data_drop.to_csv('test_v1.csv', index=False)
data_drop = data_drop.to_dict()

with open("test_v1.csv", "w") as f:
    reader = csv.reader(f)
    next(reader)
    data = []
    for row in reader:

with open("test_v1.json", "w") as f:
    json.dump(data_drop, f)