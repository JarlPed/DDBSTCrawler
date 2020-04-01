# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 12:18:39 2020

@author: jarl.robert.pedersen
"""

import re
import sqlite3

SQLcon = sqlite3.connect('./DDBST_Meta.db')
SQLCursor = SQLcon.cursor()

DDB_RN_Sequences = SQLCursor.execute('SELECT * FROM Mixure_Property_Metadata;')


Entries = []
largestSequence = 1
for tuple_item in DDB_RN_Sequences.fetchall():
    Splitted_Regs = tuple_item[0].split(',')
    Entries.append( [Splitted_Regs, item for item in tuple_item[1:], item in tuple_item[-2:] ] )
    
    if len(Splitted_Regs) > largestSequence :
        largestSequence = len(Splitted_Regs)
    
    
for Sequence_size in range(3, largestSequence + 1):
    for i in range(len(Entries)):
        if len(Entries[i][0] ) !=  Sequence_size :
            continue
        
        for j in range(len(Entries)):
            if i == j or len(Entries[j][0]) > Sequence_size - 1 + 0.01 :
                continue
            
            findBool = True
            
            for DDB_index in Entries[j][0] :
                if DDB_index not in Entries[i][0]:
                    findBool = False
                    break
            if not findBool:
                continue
            
            Entries[i][-2] -=  Entries[j][-2]
            Entries[i][-1] -=  Entries[j][-1]
            
            
            
            
