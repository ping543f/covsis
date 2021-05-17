# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 16:33:37 2020

@author: LENOVO
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
from mpl_toolkits.mplot3d import Axes3D
import math
import datetime
graph_type = '3D'

file_name_list=['au','ca', 'cn', 'fr','in','it','nz','uk','us']

for file_name in file_name_list:
    matrix = pd.read_csv(file_name+".csv", sep = ",")
    matrix = matrix.values
    print(datetime.datetime.now(), ":Processing File |======> :",file_name)
    x = [i for i in range (0, 10, 1)]
    y = [i for i in range (0, 11,1)]
    # my_yticks= ['fever', 'cough','pain','sore throat','fatigue','headache','dry cough','chills','vomiting','diarrhea','conjunctivitis']
    z = np.zeros((len(y), len(x)))

    #print (z)

    for i, record in enumerate(matrix):
        values = list(record)
        for j in range (0, len(values)):
            if values[j] == 0:
                z[i][j] = 0
            else:
                z[i][j] = np.log10(values[j])
        

    xmin, xmax = np.amin(x), np.amax(x)
    print (xmin, xmax)
    ymin, ymax = np.amin(y), np.amax(y)
    print (ymin, ymax)
    extent = (xmin, xmax, ymin, ymax)
    print (extent)

    ip1 = interp2d(x, y, z, kind='cubic')

    x2 = np.linspace(xmin, xmax, 300)
    y2 = np.linspace(ymin, ymax, 300)
    
    z2 = ip1(x2, y2)

    x2, y2 = np.meshgrid(x2, y2)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # z2[z2 != 0] = np.log10(z2[z2 != 0])
    surf = ax.plot_surface(x2, y2, z2, rstride=1, cstride=1, cmap='viridis', 
                    edgecolor='none', alpha = 1)
    ax.view_init(azim = 120)

    # Add a color bar which maps values to colors.
    #fig.colorbar(surf, shrink=0.5, aspect=10)
    # Now adding the colorbar
    cbaxes = fig.add_axes([0.88, 0.2, 0.03, 0.6]) 
    cb = plt.colorbar(surf, cax = cbaxes)  
    cb.set_clim(0.0, 4.0)
    cb.ax.tick_params(labelsize=12)
    
    plt.rcParams["figure.figsize"] = (12, 12)
    plt.rcParams["axes.edgecolor"] = "0.15"
    plt.rcParams["axes.linewidth"]  = 2
    plt.rcParams["axes.facecolor"] = "white"
    #ax.set_yticks([1,2,3,4,5,6,7,8,9,10,11])
    # ax.set_yticklabels(['fever', 'cough','pain','sore throat','fatigue','headache','dry cough','chills','vomiting','diarrhea','conjunctivitis'])
    
    ax.set_yticks([0,1,2,3,4,5,6,7,8,9,10])
    ax.set_yticklabels(['Fever','Cough','Pain','Sore throat','Fatigue','Headache','Dry cough','Chills','Diarrhea','Vomiting','Conjunctivitis'])
    ax.set_xticks([0,1,2,3,4,5,6,7,8,9])
    ax.set_xticklabels(['15D', '30D', '45D', '60D', '75D', '90D', '105D', '120D', '135D', '150D'])
    #plt.xlabel ("% of dataset length", fontsize=14)
    #plt.ylabel ("Minimum support", fontsize=14)
    #plt.zlabel ("Accuracy", fontsize=14) 
    #plt.tick_params(labelsize=14)
    ax.dist=12
    ax.tick_params(direction='out', length=3, width=10.5, colors='k',
            grid_color='k', grid_alpha=0.5, labelsize = 12, labelrotation=90)
    #ax.view_init(azim=120)
    
    plt.savefig(file_name+'_3D_rot0.svg', dpi = 300)
    # plt.savefig('uk_3D.eps', dpi = 300)
    plt.savefig(file_name+'_3D_rot0.png', dpi = 300)
    # plt.show()
    print(datetime.datetime.now(),file_name, " Processing is done!\n")