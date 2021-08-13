import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import matplotlib.font_manager
import copy

'''CHN	USA	RUS	IND	GBR	BRA	DEU	ITA	ESP	UAE
0.369450139	0.319675042	0.329860679	0.37968149	0.319675042	0.337415898	0.342693596	0.359363427	0.348349922	0.366332708
0.280505169	0.257194332	0.219039797	0.287646028	0.257194332	0.265513876	0.247112831	0.281144124	0.25420277	0.270604904
0.069575373	0.113695432	0.260514302	0.121383653	0.113695432	0.183850655	0.127504669	0.086606687	0.108923206	0.04844905
0.074982258	0.082715768	0.044099111	0.062474014	0.082715768	0.075156647	0.062085982	0.065118239	0.057933058	0.105132734
0.0407201	0.055826725	0.029526772	0.032893816	0.055826725	0.036073136	0.043462837	0.03811359	0.033903604	0.012306523
0.042897442	0.043646329	0.039775102	0.035520272	0.043646329	0.039558393	0.059144162	0.04158178	0.053335865	0.078828407
0.039685626	0.037148135	0.01825724	0.032876413	0.037148135	0.026280717	0.034545537	0.047726821	0.034101564	0.009213631
0.022366827	0.029871295	0.016192929	0.014134395	0.029871295	0.012644728	0.031435466	0.02768309	0.037750557	0.037792134
0.03229202	0.025376316	0.018792903	0.009717775	0.025376316	0.006336196	0.027341948	0.026155186	0.032843652	0.044387056
0.022870298	0.028530247	0.022328199	0.022529867	0.028530247	0.014714592	0.020510005	0.019731413	0.028353792	0.014872349
0.004654748	0.006320377	0.001612965	0.001142277	0.006320377	0.002455162	0.004162967	0.006775642	0.010302009	0.012080504
'''

plt.rcParams["font.family"] = 'Arial Narrow'

scolors = {'Fever': '#1f77b4', 'Dry Cough': '#ff7f0e', 'Tiredness or Fatigue': '#2ca02c', 
           'Aches and Muscle Pains': '#d62728', 'Sore Throat': '#9467bd', 'Diarrhoea': '#8c564b', 
           'Conjunctivitis': '#e377c2', 'Headache': '#7f7f7f', 'Loss of Taste or Smell': '#bcbd22', 
           'Skin Rash': '#17becf', 'Shortness of Breath': '#aec7e8',  'Chest Pain': '#aec7e8', 
           'Loss of Speech': '#ffbb78'}

recom_dic = {'Fever': 0, 'Dry Cough': 0, 'Tiredness or Fatigue': 0, 'Aches and Muscle Pains': 0, 
                  'Sore Throat': 0, 'Diarrhoea': 0, 'Conjunctivitis': 0, 'Headache': 0, 'Loss of Taste or Smell': 0, 
                  'Skin Rash': 0, 'Shortness of Breath': 0, 'Chest Pain': 0, 'Loss of Speech': 0}
 
data = pd.read_csv("histogram_data.csv")
print (data)

'''
#r = [0]
raw_data = {'Fever': [0.343484839,	0.310505421,	0.297468529,	0.318883985,	0.286699547,	0.292291922,	0.31158903,	0.317841205,	0.266885392,	0.330371986], \
        'Dry Cough': [0.304219562,	0.264454347,	0.216860837,	0.273230401,	0.249820152,	0.238678421,	0.254987991,	0.28820907,	0.224648504,	0.254237761], \
        'Tiredness or Fatigue': [0.045396326,	0.048766486,	0.030960062,	0.03262238,	0.057634432,	0.028532504,	0.05151915,	0.044908536,	0.031619075,	0.00913613], \
        'Aches and Muscle Pains': [0.024355095,	0.024115993,	0.018754855,	0.01346499,	0.019944226,	0.018574397,	0.03344547,	0.023443444,	0.028930236,	0.01325199], \
        'Sore Throat': [0.078430991,	0.062117338,	0.045211515,	0.059181715,	0.078068857,	0.061739124,	0.064970218,	0.066322651,	0.056527627,	0.095922956], \
        'Diarrhoea': [0.016324778,	0.00527191,	0.008087348,	0.025920971,	0.030178438,	0.011056481,	0.017388959,	0.015956693,	0.02148927,	0.002776417], \
        'Conjunctivitis': [0.005310548,	0.0047264,	0.002571245,	0.001471321,	0.006866945,	0.002290365,	0.003825716,	0.00769365,	0.010998491,	0.011441667], \
        'Headache': [0.045807245,	0.046906475,	0.031455428,	0.033317582,	0.043795629,	0.031910119,	0.060767451,	0.042846421,	0.048209197,	0.068849264], \
        'Loss of Taste or Smell': [7.20E-09,	0.000328659,	0,	0,	5.63E-06,	0,	0.002521247,	2.15E-08,	0,	0], \
        'Skin Rash': [0.011876294,	0.030056833,	0.020346315,	0.008115454,	0.032280861,	0.031396718,	0.01979306,	0.036177671,	0.05906931,	0], \
        'Shortness of Breath': [0.005151664,	0.005756755,	0.002486951,	0.005779804,	0.005576875,	0.004153886,	0.005836889,	0.00366496,	0.002551065,	0.001997799],\
        'Chest Pain': [0.11049694,	0.183056733,	0.23688946,	0.139393425,	0.177045699,	0.187255607,	0.149215854,	0.141775328,	0.164852196,	0.058049042],\
        'Loss of Speech': [0.009145711,	0.013936651,	0.011984379,	0.011694895,	0.012082712,	0.015197379,	0.024138968,	0.01116035,	0.007296559,	0.000118835]}
df = pd.DataFrame(raw_data)

# From raw value to percentage
totals = [i+j+k+l+m+n+o+p+q+r+s+t+u for i,j,k,l,m,n,o,p,q,r,s,t,u in zip(df['Fever'], 
df['Dry Cough'], df['Tiredness or Fatigue'], df['Aches and Muscle Pains'], df['Sore Throat'], df['Diarrhoea'], 
df['Conjunctivitis'], df['Headache'], df['Loss of Taste or Smell'], df['Skin Rash'], df['Shortness of Breath'],
df['Chest Pain'], df['Loss of Speech'])]
Fever = [i / j * 100 for i,j in zip(df['Fever'], totals)]
DryCough = [i / j * 100 for i,j in zip(df['Dry Cough'], totals)]
TirednessOrFatigue = [i / j * 100 for i,j in zip(df['Tiredness or Fatigue'], totals)]
AchesAndMusclePains = [i / j * 100 for i,j in zip(df['Aches and Muscle Pains'], totals)]
SoreThroat = [i / j * 100 for i,j in zip(df['Sore Throat'], totals)]
Diarrhoea = [i / j * 100 for i,j in zip(df['Diarrhoea'], totals)]
Conjunctivitis = [i / j * 100 for i,j in zip(df['Conjunctivitis'], totals)]
Headache = [i / j * 100 for i,j in zip(df['Headache'], totals)]
LossOfTaste = [i / j * 100 for i,j in zip(df['Loss of Taste or Smell'], totals)]
SkinRash = [i / j * 100 for i,j in zip(df['Skin Rash'], totals)]
ShortnessOfBreath = [i / j * 100 for i,j in zip(df['Shortness of Breath'], totals)]
ChestPain = [i / j * 100 for i,j in zip(df['Chest Pain'], totals)]
LossOfSpeech = [i / j * 100 for i,j in zip(df['Loss of Speech'], totals)]
'''

# Data
r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# plot
barWidth = 0.85
names = ['CHN',  'USA', 'RUS', 'IND', 'GBR', 'BRA', 'DEU', 'ITA', 'ESP', 'UAE']
#names = ('CHN',  'USA', 'RUS', 'IND', 'GBR', 'BRA', 'DEU', 'ITA', 'ESP', 'UAE')

symp = data['Symptoms']
#print (symp)

del data['Symptoms']

data = data.values
#print (data)

fdata = {}
for country in names:
    fdata[country] =  copy.deepcopy(recom_dic)
    
#print (fdata)

for i,record in enumerate(data):
    print (record)
    for j, country in enumerate(names):
        fdata[country][symp[i]] = record[j]

print (fdata)

for country in fdata:
    fdata[country] = dict(sorted(fdata[country].items(), key=lambda x: x[1], reverse = True))

#print (fdata)

r = [x for x in range (len(names))]

def calculateBottom (c, s):
    sum_ = 0
    record = fdata[c]
    for key in record:
        if key != s:
            sum_ += record[key]
        else:
            break
    return sum_

print (fdata)

for i, key in enumerate(fdata):
    record = fdata[key]
    print (record)
    for s in record:
        if i == 0:
            plt.bar(i, record[s], bottom = calculateBottom(key, s), color=scolors[s], edgecolor='white', width=barWidth, label = s)
        else:
            plt.bar(i, record[s], bottom = calculateBottom(key, s), color=scolors[s], edgecolor='white', width=barWidth)

'''
plt.bar(r, Fever, color=scolors['Fever'], edgecolor='white', width=barWidth, label="Fever")
plt.bar(r, DryCough, bottom=Fever, color=scolors[1], edgecolor='white',  width=barWidth, label="Dry Cough")
plt.bar(r, TirednessOrFatigue, bottom=[i+j for i,j in zip(Fever, DryCough)], color=scolors[2], edgecolor='White', 
width=barWidth, label="Tiredness or Fatigue")
plt.bar(r, AchesAndMusclePains, bottom=[i+j+k for i,j,k in zip(Fever, DryCough, TirednessOrFatigue)], 
color=scolors[3], edgecolor='white', width=barWidth, label="Aches and Muscle Pains")
plt.bar(r, SoreThroat, bottom=[i+j+k+l for i,j,k,l in zip(Fever, DryCough, TirednessOrFatigue, 
AchesAndMusclePains)], color=scolors[4], edgecolor='white', width=barWidth, label="Sore Throat")
plt.bar(r, Diarrhoea, bottom=[i+j+k+l+m for i,j,k,l,m in zip(Fever, DryCough, TirednessOrFatigue, 
AchesAndMusclePains, SoreThroat)], color=scolors[5], edgecolor='white', width=barWidth, 
label="Diarrhoea")
plt.bar(r, Conjunctivitis, bottom=[i+j+k+l+m+n for i,j,k,l,m,n in zip(Fever, DryCough, TirednessOrFatigue, 
AchesAndMusclePains, SoreThroat, Diarrhoea)], color=scolors[6], edgecolor='white', 
width=barWidth, label="Conjunctivitis")
plt.bar(r, Headache, bottom=[i+j+k+l+m+n+o for i,j,k,l,m,n,o in zip(Fever, DryCough, TirednessOrFatigue, 
AchesAndMusclePains, SoreThroat, Diarrhoea, Conjunctivitis)], color=scolors[7], 
edgecolor='white', width=barWidth, label="Headache")
plt.bar(r, LossOfTaste, bottom=[i+j+k+l+m+n+o+p for i,j,k,l,m,n,o,p in zip(Fever, DryCough, TirednessOrFatigue, 
AchesAndMusclePains, SoreThroat, Diarrhoea, Conjunctivitis, Headache)], color=scolors[8], 
edgecolor='white', width=barWidth, label="Loss of Taste or Smell")
plt.bar(r, SkinRash, bottom=[i+j+k+l+m+n+o+p+q for i,j,k,l,m,n,o,p,q in zip(Fever, DryCough, TirednessOrFatigue, 
AchesAndMusclePains, SoreThroat, Diarrhoea, Conjunctivitis, Headache, LossOfTaste)], color=scolors[9], 
edgecolor='white', width=barWidth, label="Skin Rash")
plt.bar(r, ShortnessOfBreath, bottom=[i+j+k+l+m+n+o+p+q+r for i,j,k,l,m,n,o,p,q,r in zip(Fever, DryCough, TirednessOrFatigue, 
AchesAndMusclePains, SoreThroat, Diarrhoea, Conjunctivitis, Headache, LossOfTaste, SkinRash)], color=scolors[10], 
edgecolor='white', width=barWidth, label="Shortness of Breath")
plt.bar(r, ChestPain, bottom=[i+j+k+l+m+n+o+p+q+r+s for i,j,k,l,m,n,o,p,q,r,s in zip(Fever, DryCough, TirednessOrFatigue, 
AchesAndMusclePains, SoreThroat, Diarrhoea, Conjunctivitis, Headache, LossOfTaste, SkinRash, ShortnessOfBreath)], color=scolors[11], 
edgecolor='white', width=barWidth, label="Chest Pain")
plt.bar(r, LossOfSpeech, bottom=[i+j+k+l+m+n+o+p+q+r+s+t for i,j,k,l,m,n,o,p,q,r,s,t in zip(Fever, DryCough, TirednessOrFatigue, 
AchesAndMusclePains, SoreThroat, Diarrhoea, Conjunctivitis, Headache, LossOfTaste, SkinRash, ShortnessOfBreath, ChestPain)], color=scolors[12], 
edgecolor='white', width=barWidth, label="Loss of Speech")
'''

# Custom x axis
plt.xticks(r, names)
plt.xlabel("Country name")

# Custom y axis
plt.ylabel("$W_L$ values of Symptoms in Parcentile")

# Add a legend
plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)

plt.savefig("CountryVsSymptom.png", dpi=600,
            transparent=True,
            bbox_inches='tight', pad_inches=0.02)
    
plt.savefig("CountryVsSymptom.svg", dpi=600,
            transparent=True,
            bbox_inches='tight', pad_inches=0.02)

# Show graphic
plt.show()