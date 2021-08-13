import os
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
from mpl_toolkits.mplot3d import Axes3D
import copy

path = r'C:\Users\LENOVO\Desktop\KnowledeMap\weight_cal'
#fig_path = r'C:\Users\LENOVO\Desktop\Behavioral Trust Model\trust model\Fig_and_Res\figure\optimization\iFP'

####################
# Utility function
####################
def findTrustScore (cos, cts):
    #alpha is the trust border 
    alpha = 0.5
        
    if len(cos & cts) > 0:
        score = (1 - alpha) * (len(cos & cts) / len (cos | cts)) + alpha
    else:
        score = alpha / len(cos | cts)
    return score

def findPriorityScore (r, max_rank, min_rank):
    val = (max_rank - r + 1) / (max_rank - min_rank + 1)
    return val

def findSymptomScore (sym_set, recom_sym):
    count = 0
    for sym in sym_set:
        split = sym.split()
        found = False
        for word in split:
            for symp in recom_sym:
                if word in symp:
                    count += 1
                    found = True
                    break
            if found:
                break
                    
    return count / len(recom_sym)
  
##################
# Calculate score
##################
def CalculateScore ():
    data = pd.read_csv(path + r'\data_revised.csv', sep = ',')
    rank = pd.read_csv(path + r'\alexa_domain_rank_map.csv')   
    
    ct, co, symptom, domain = data['Country'], data['Source_country'], data['Symp'], data['Domain']
    dmn, rnk = rank['Domain'], rank['Rank']
    dmn = list(dmn.values)
    rnk = rnk.values
        
    #max_rank = max(rnk)
    max_rank = 2500
    min_rank = min(rnk)
    
    #print (max_rank, min_rank)
    
    recom_symp = {'fever', 'dry cough', 'tiredness or fatigue', 'aches and muscles', 'sore throat',
                  'diarrhoea', 'conjunctivitis', 'headache', 'loss of taste or smell', 
                  'a rash on skin or discolouration of fingers or toes', 'difficulty breathing or shortness of breath',
                  'chest pain or pressure', 'loss of speech or movement'}
            
    recom_dic = {'fever': 0, 'dry cough': 0, 'tiredness or fatigue': 0, 'aches and muscles': 0, 'sore throat': 0,
                  'diarrhoea': 0, 'conjunctivitis': 0, 'headache': 0, 'loss of taste or smell': 0, 
                  'a rash on skin or discolouration of fingers or toes': 0, 
                  'difficulty breathing or shortness of breath': 0,
                  'chest pain or pressure': 0, 'loss of speech or movement': 0}
    
    data_dic = {}
    
    for i in range(len(rnk)): 
        rnk[i] = int(rnk[i]) 
        
    for i in range (len(ct)):
        coi = co[i].split(';')
        #coi.remove(' ')
        cos = set(coi)
        
        cti = ct[i].split(';')
        
        if ' ' in cti:
            cti.remove(' ')
        if '' in cti:
            cti.remove('')
        
        cts = set(cti)
        
        trust_score = findTrustScore(cos, cts)
        #print (cos, cts, trust_score)
        
        priority_score = 0
        if domain[i] in dmn:
            ind = dmn.index(domain[i])
            r = rnk[ind]
            if r > max_rank:
                r = max_rank
            priority_score = findPriorityScore (r, max_rank, min_rank)

        symp_list = symptom[i].split(';')
        #coi.remove(' ')
        
        if ' ' in symp_list:
            symp_list.remove(' ')
        if '' in symp_list:
            symp_list.remove('')
            
        symp_list = [x.lower() for x in symp_list]
        symp_set = set(symp_list)
                
        symptom_score = findSymptomScore (symp_set, recom_symp)
        #print (symp_set)
                
        weight = trust_score * priority_score * symptom_score
        #print (trust_score, priority_score, symptom_score, weight)
        
        cu = cos | cts
        for country in cu:
            if country not in data_dic:
                data_dic[country] = copy.deepcopy(recom_dic)
        
            for sym in symp_set:
                split = sym.split()
                #print (split)
                found = False
                for word in split:
                    for symp in recom_symp:
                        #print (word, symp)
                        if word in symp:
                            #print (data_dic[country][symp])
                            data_dic[country][symp] = data_dic[country][symp] + weight
                            #print (data_dic[country][symp])
                            found = True
                            break
                    if found:
                        break
                   
    ####################
    # Normalized weight
    ######################
    for country in data_dic:
        symp = data_dic[country]
        sum_ = 0
        N = 0
        for key in symp:
            sum_ += symp[key]
            if symp[key] > 0:
                N += 1
        
        for key in symp:
            if sum_ != 0:
                wl = (symp[key] / sum_) * (N / len(recom_symp))
            else:
                wl = 0
            symp[key] = wl
            
    cunt_list = []
    for country in data_dic:
        symp = data_dic[country]
        
        cnt = 0
        for key in symp:
            if symp[key] == 0:
                cnt += 1
        if cnt > 12:
            cunt_list.append(country)
            
    for country in cunt_list:
        del data_dic[country]
    
    print (data_dic)
    print (len(data_dic))
    
    lw = open("localWeight.csv", mode="w", encoding="utf-8")
    for country in data_dic:
        symp = data_dic[country]
        lw.writelines(country + ",")
        for key in symp:
            lw.writelines(key + "," + str(symp[key]) + ",")
        lw.write("\n")
    lw.close()
    
    gwf = open("globalWeight.csv", mode="w", encoding="utf-8")
    gw = np.zeros((1, len(recom_symp)))
    for country in data_dic:
        symp = data_dic[country]
        i = 0
        for key in symp:
            gw[0][i] += symp[key]
            i += 1
            
    for i in range (len(recom_symp)):
        sum_ += gw[0][i]
        
    for i in range (len(recom_symp)):
        gw[0][i] = gw[0][i] / sum_
    

    for i in range (len(recom_symp)):
        gwf.writelines (str(gw[0][i]) + ",")
    gwf.write ("\n")
    gwf.close()    
    print (gw)
            
    '''
    for country in data_dic:
        for symp in country:
            print (country, symp, symp.values())
    '''

if __name__ == "__main__":
    CalculateScore()        
    
    
    #trustFactor = 
    #score = 

