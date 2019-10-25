thon# -*- coding: utf-8 -*-
"""
Created on Fri May 24 15:20:18 2019

@author: jarl
"""

from matplotlib import pyplot as plt

import numpy as np

from sympy import Symbol

import os

import re

import json 

PC_dir = './DB/Pure Component Properties (Several Properties)'

json_df = {}
T_c = []
P_c = []
V_m_c = []
R = 8.314
Z_c = 0.307401 # Symbol('Z_c')

for fileName in os.listdir(PC_dir):
    if fileName[-5:] == '.json':
        #json_files.append(fileName)
        pf = open(PC_dir + '//' + fileName, 'r')
        json_df.update(  {fileName[:-5] : json.load(pf) } )
        pf.close()
        

for key in json_df.keys():
    content = json_df[key]
    for prop in content.keys():
        if prop == 'Critical Data':
            for i in range(len(content[prop]['T [K]'])):
                if ( re.match( '\d' , content[prop]['T [K]'][i]) and re.match( '\d' , content[prop]['P [kPa]'][i])   ):
                    T_c.append( float( content[prop]['T [K]'][i] ) )
                    P_c.append( float( content[prop]['P [kPa]'][i]) )
                    V_m_c.append(  Z_c *R *  T_c[-1] / P_c[-1]   )
        if prop == "Vapor Pressure" :
            np.interp(0.7*)
                    
plt.figure()
plt.scatter(P_c, T_c)


