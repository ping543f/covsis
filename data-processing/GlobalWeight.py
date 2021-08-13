# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 01:41:44 2020

@author: LENOVO
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import matplotlib.font_manager
import seaborn as sns

plt.rcParams["font.family"] = 'Arial Narrow'

scolors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8']   

wg = [38.51705294,	26.02050523,	 17.23308656,	4.346923678,  3.602608714,  3.061173525,	
      2.099876125, 1.933387308,	1.287440557, 1.140551453, 0.59945767,	0.1532513,
      0.004684946 ]

symptoms = ['Fever', 'Dry cough', 'Chest pain', 'Sore Throat', 'Headache', 'Tiredness or Fatigue',  'Skin Rash',
                    'Aches and Muscle Pains', 'Loss of speech', 'Diarrhoea', 'Shortness of Breath', 
                    'Conjunctivitis',  'Loss of taste or smell']

#scolors = {'Fever': '#1f77b4', 'Dry Cough': '#ff7f0e', 'Tiredness or Fatigue': '#2ca02c', 
#           'Aches and Muscle Pains': '#d62728', 'Sore Throat': '#9467bd', 'Diarrhoea': '#8c564b', 
#           'Conjunctivitis': '#e377c2', 'Headache': '#7f7f7f', 'Loss of Taste or Smell': '#bcbd22', 
#           'Skin Rash': '#17becf', 'Shortness of Breath': '#aec7e8',  'Chest Pain': '#aec7e8', 
#           'Loss of Speech': '#ffbb78'}

scolors = ['#1f77b4', '#ff7f0e', '#aec7e8', '#9467bd', '#7f7f7f', '#2ca02c', '#17becf', '#d62728', 
           '#ffbb78', '#8c564b', '#aec7e8', '#e377c2', '#bcbd22']   

raw_data = {'Symptom': symptoms, 'Weight': wg}

df = pd.DataFrame.from_dict(raw_data)

print (df.head(5))

ax = sns.barplot(x="Weight", y="Symptom", data=df, palette = sns.color_palette(scolors))
ax.grid('on')
#plt.title('Distribution of  Configurations')
plt.xlabel('$W_G$ values of Symptoms in Parcentile')

plt.savefig("GlobalScore.png", dpi=600,
            transparent=True,
            bbox_inches='tight', pad_inches=0.02)
    
plt.savefig("GlobalScore.svg", dpi=600,
            transparent=True,
            bbox_inches='tight', pad_inches=0.02)

plt.show()