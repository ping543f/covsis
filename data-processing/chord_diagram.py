# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 14:58:44 2020

@author: LENOVO
"""


###################

# chord diagram

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import matplotlib.font_manager

LW = 0.8

def polar2xy(r, theta):
    return np.array([r*np.cos(theta), r*np.sin(theta)])

def hex2rgb(c):
    return tuple(int(c[i:i+2], 16)/256.0 for i in (1, 3 ,5))

def IdeogramArc(start=0, end=60, radius=1.0, width=0.2, ax=None, color=(1,0,0)):
    # start, end should be in [0, 360)
    if start > end:
        start, end = end, start

    start *= np.pi/180.
    end *= np.pi/180.

    # optimal distance to the control points
    # https://stackoverflow.com/questions/1734745/how-to-create-circle-with-b%C3%A9zier-curves
    opt = 4./3. * np.tan((end-start)/ 4.) * radius
    inner = radius*(1-width)
    verts = [
        polar2xy(radius, start),
        polar2xy(radius, start) + polar2xy(opt, start+0.5*np.pi),
        polar2xy(radius, end) + polar2xy(opt, end-0.5*np.pi),
        polar2xy(radius, end),
        polar2xy(inner, end),
        polar2xy(inner, end) + polar2xy(opt*(1-width), end-0.5*np.pi),
        polar2xy(inner, start) + polar2xy(opt*(1-width), start+0.5*np.pi),
        polar2xy(inner, start),
        polar2xy(radius, start),
        ]

    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CLOSEPOLY,
             ]

    if ax == None:
        return verts, codes
    else:
        path = Path(verts, codes)
        #patch = patches.PathPatch(path, facecolor=color+(0.5,), edgecolor=color+(0.4,), lw=LW)
        patch = patches.PathPatch(path, facecolor=color+(0.5,), edgecolor=color+(0.4,), lw=LW)
        ax.add_patch(patch)

def ChordArc(start1=0, end1=60, start2=180, end2=240, radius=1.0, chordwidth=0.7, ax=None, color=(1,0,0)):
    # start, end should be in [0, 360)
    if start1 > end1:
        start1, end1 = end1, start1
    if start2 > end2:
        start2, end2 = end2, start2
        
    start1 *= np.pi/180.
    end1 *= np.pi/180.
    start2 *= np.pi/180.
    end2 *= np.pi/180.

    opt1 = 4./3. * np.tan((end1-start1)/ 4.) * radius
    opt2 = 4./3. * np.tan((end2-start2)/ 4.) * radius
    rchord = radius * (1-chordwidth)

    verts = [
        polar2xy(radius, start1),
        polar2xy(radius, start1) + polar2xy(opt1, start1+0.5*np.pi),
        polar2xy(radius, end1) + polar2xy(opt1, end1-0.5*np.pi),
        polar2xy(radius, end1),
        polar2xy(rchord, end1),
        polar2xy(rchord, start2),
        polar2xy(radius, start2),
        polar2xy(radius, start2) + polar2xy(opt2, start2+0.5*np.pi),
        polar2xy(radius, end2) + polar2xy(opt2, end2-0.5*np.pi),
        polar2xy(radius, end2),
        polar2xy(rchord, end2),
        polar2xy(rchord, start1),
        polar2xy(radius, start1),
        ]

    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             ]



    if ax == None:
        return verts, codes
    else:
        path = Path(verts, codes)
       # patch = patches.PathPatch(path, facecolor=color+(0.5,), edgecolor=color+(0.4,), lw=LW)
        patch = patches.PathPatch(path, facecolor=color+(0.5,), edgecolor=color+(0.4,), lw=LW)
        ax.add_patch(patch)

'''
def selfChordArc(start=0, end=60, radius=1.0, chordwidth=0.7, ax=None, color=(1,0,0)):
    # start, end should be in [0, 360)
    if start > end:
        start, end = end, start

    start *= np.pi/180.
    end *= np.pi/180.
    opt = 4./3. * np.tan((end-start)/ 4.) * radius
    rchord = radius * (1-chordwidth)

    verts = [
        polar2xy(radius, start),
        polar2xy(radius, start) + polar2xy(opt, start+0.5*np.pi),
        polar2xy(radius, end) + polar2xy(opt, end-0.5*np.pi),
        polar2xy(radius, end),
        polar2xy(rchord, end),
        polar2xy(rchord, start),
        polar2xy(radius, start),
        ]

    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             ]

    if ax == None:
        return verts, codes
    else:
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=color+(0.8,), edgecolor=color, lw=LW)
        ax.add_patch(patch)
'''

def chordDiagram(X, ax, symptom_colors=None, country_colors=None, width=0.1, pad=2, chordwidth=0.7):

    """Plot a chord diagram
    Parameters
    ----------
    X :
        flux data, X[i, j] is the flux from i to j
    ax :
        matplotlib `axes` to show the plot
    colors : optional
        user defined colors in rgb format. Use function hex2rgb() to convert hex color to rgb color. Default: d3.js category10
    width : optional
        width/thickness of the ideogram arc
    pad : optional
        gap pad between two neighboring ideogram arcs, unit: degree, default: 2 degree
    chordwidth : optional
        position of the control points for the chords, controlling the shape of the chords
    """

    # X[i, j]:  i -> j
    x = X.sum(axis = 1) # sum over rows
    print (x)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    
    if symptom_colors is None:
    # use d3.js category10 https://github.com/d3/d3-3.x-api-reference/blob/master/Ordinal-Scales.md#category10
        symptom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8',
                  '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#9467bd']        
                  
    if country_colors is None:
    # use d3.js category10 https://github.com/d3/d3-3.x-api-reference/blob/master/Ordinal-Scales.md#category10
        country_colors = ['#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', 
                         '#9edae5', '#393b79', '#5254a3', '#6b6ecf', '#9c9ede',
                         '#637939', '#8ca252', '#b5cf6b', '#cedb9c', '#8c6d31',
                         '#bd9e39', '#e7ba52', '#e7cb94', '#843c39', '#ad494a',
                         '#d6616b', '#e7969c', '#7b4173', '#a55194', '#ce6dbd',
                         '#de9ed6', '#3182bd', '#6baed6', '#9ecae1', '#c6dbef',
                         '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354',
                         '#74c476', '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8',
                         '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd']
        

    # find position for each start and end
    y = x/np.sum(x).astype(float) * (150 - pad*len(x))

    pos = {}
    arc = []
    nodePos = []
    rotate = 285
    start = 0 + rotate

    for i in range(len(x)):        
        end = start + y[i]
        arc.append((start, end))
        angle = 0.5*(start+end)
        
        nodePos.append(tuple(polar2xy(1.1, angle*np.pi/180.)) + (angle,))
        z = (X[i, :]/x[i].astype(float)) * (end - start)
        ids = np.argsort(z)
        
        z0 = start 
        
        for j in ids:
            pos[(i, j)] = (z0, z0+z[j])
            z0 += z[j]
        
        start = end + pad

    for i in range(len(x)):
        start, end = arc[i]
        IdeogramArc(start=start, end=end, radius=1, ax=ax, color=hex2rgb(symptom_colors[i]), width=width)
        #start, end = pos[(i,i)]
        #selfChordArc(start, end, radius=1.-width, color=colors[i], chordwidth=chordwidth*0.7, ax=ax)

        '''
        for j in range(i):
            color = symptom_colors[i]
            if X[i, j] > X[j, i]:
                color = symptom_colors[j]

            start1, end1 = pos[(i,j)]
            start2, end2 = pos[(j,i)]

            #ChordArc(start1, end1, start2, end2, radius=1.-width, color=colors[i], chordwidth=chordwidth, ax=ax) 
        '''
        
    x1 = X.sum(axis = 0) # sum over columns
    
    # find position for each start and end
    y1 = x1/np.sum(x1).astype(float) * (150 - pad*len(x1))

    pos1 = {}
    arc1 = []
    nodePos1 = []
    rotate = 105
    start = 0 + rotate

    for i in range(len(x1)):        
        end = start + y1[i]
        arc1.append((start, end))
        angle = 0.5*(start+end)
        
        nodePos1.append(tuple(polar2xy(1.1, angle*np.pi/180.)) + (angle,))
        z = (X[:, i]/x1[i].astype(float)) * (end - start)
        ids = np.argsort(z)
        
        z0 = start 
        
        for j in ids:
            pos1[(i, j)] = (z0, z0+z[j])
            z0 += z[j]
            
        start = end + pad

    for i in range(len(x1)):
        start, end = arc1[i]
        IdeogramArc(start=start, end=end, radius=1, ax=ax, color=hex2rgb(country_colors[i]), width=width)
        #start, end = pos[(i,i)]
        #selfChordArc(start, end, radius=1.-width, color=colors[i], chordwidth=chordwidth*0.7, ax=ax)
        
        '''
        for j in range(i):
            color = symptom_colors[i]
            if X[i, j] > X[j, i]:
                color = symptom_colors[j]

            start1, end1 = pos[(i,j)]
            start2, end2 = pos[(j,i)]
            
        #ChordArc(start1, end1, start2, end2, radius=1.-width, color=colors[i], chordwidth=chordwidth, ax=ax) 
        '''
    
    for i in range (len(x)):
        for j in range (len(x1)):
             start1, end1 = pos[(i,j)]
             start2, end2 = pos1[(j,i)]
             
             ChordArc(start1, end1, start2, end2, radius=1.-width, color=hex2rgb(symptom_colors[i]), chordwidth=chordwidth, ax=ax) 
                        
    return nodePos, nodePos1

##################################

if __name__ == "__main__":
    
    plt.rcParams["font.family"] = 'Arial Narrow'
    
    fig = plt.figure(figsize=(6,6))
      
    '''
    flux = np.array([[11975,  5871, 8916, 2868],
      [ 1951, 10048, 2060, 6171],
      [ 8010, 16145, 8090, 8045],
      [ 1013,   990, 940, 6907],
      [ 1031,  1990, 1940, 9076]
    ])
    '''
    
    df = pd.read_csv("SpatialSymptoms.csv")
    print(df.head(5))
    
    symptoms = df['Symptoms'].tolist()
    print (symptoms)
    countries = df.columns.tolist()[1:]
    print (countries)
    
    df = df.drop(['Symptoms'], axis = 1)
    matrix = df.values
    print (matrix)
        
    ax = plt.axes([0,0,1,1])
    print (ax)
    ax.axis('off')
    
    nodePos, nodePos1 = chordDiagram(matrix, ax)
    ax.axis('off')
    
    prop = dict(fontsize=7, ha='center', va='center', )
    nodes = symptoms

    for i in range(len(symptoms)):
        ax.text(nodePos[i][0], nodePos[i][1], nodes[i], rotation=nodePos[i][2], **prop)
        
    nodes = countries

    for i in range(len(countries)):
        ax.text(nodePos1[i][0], nodePos1[i][1], nodes[i], rotation=nodePos1[i][2] + 180, **prop)
        
    plt.savefig("Fig-Country-Symptom-Map.png", dpi=600,
            transparent=True,
            bbox_inches='tight', pad_inches=0.02)
    
    plt.savefig("Fig-Country-Symptom-Map.svg", dpi=600,
            transparent=True,
            bbox_inches='tight', pad_inches=0.02)