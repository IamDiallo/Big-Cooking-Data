# %%
import pandas
import csv
import numpy as np
import ast
import collections
import matplotlib.pyplot as plt

# %%
# read the column ingredients
colnames = ['ingredients']
data = pandas.read_csv('test_1.csv', usecols=colnames)

# %%
# retrieves the ingredients
ingredients = []
for k,v in data.items():
    print(k)
    for x in v:
        try:   
            if x!=np.nan:
                res = ast.literal_eval(x)
                ingredients.append(res)
        except:
            print(x)
#print(ingredients)

# %%
#counter the number of appearance of an ingredient
list_ingre = []
for n in ingredients:
    for x in n:
        list_ingre.append(x['nom_ingre'])
counter=collections.Counter(list_ingre)
print(len(counter))
#print(counter)

# %%
# remove ingrediens with less than 5 appearances
usedIngre = []
for x, y in counter.items():
    if y >=5:
        usedIngre.append(x) 
print(len(usedIngre))
#print(usedIngre)

# %%
colnames = ['nom','ingredients']
data = pandas.read_csv('test_1.csv', usecols=colnames)
# creatVector(usedIngre,data['nom'])

# %%
# Data to plot
labels = []
sizes = []
for x, y in counter.items():
    if y >=100:
        labels.append(x)
        sizes.append(y)

# Plot
plt.pie(sizes, labels=labels, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)

plt.axis('equal')
plt.show()

# %%



