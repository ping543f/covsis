# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 16:24:26 2020

@author: LENOVO
"""

import pandas as pd
import math

path = r'C:\Users\LENOVO\Desktop\KnowledeMap\weight_cal'

data = pd.read_csv(path + r'\localWeightFormat.csv', sep = ',')
print (data.head())

country = data['country']
del data['country']
data = list(data.values.tolist())

gw = [0.385170529, 0.260205052, 0.030611735,	0.019333873,  0.043469237, 0.011405515, 0.01532513, 0.036026087,	4.68E-05,	0.020998761,  0.005994577,  0.172330866,	0.012874406]
gw2 = [x * x for x in gw]
print (gw2)

similarity = {}
file = open("similarity.csv", 'w+')

for i, record in enumerate(data):
    sum_ = 0
    ls = 0
    
    for j in range (len(record)):
        sum_ += record[j] * gw[j]
        ls += record[j] * record[j]
    
    gs = sum(gw2)
    simi = sum_ / (math.sqrt(ls) * math.sqrt(gs))
    similarity[country[i]] = simi
    file.write (country[i] + ", " + str(simi) + "\n")
    
file.close()
    




        





