# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 08:37:26 2020

@author: jarl.robert.pedersen
"""

import requests
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import sqlite3
import os
import time
import warnings

from fake_useragent import UserAgent



def responce_manager(url, headers):
    try:
        #time.sleep(1)
        return requests.get(url, headers=headers )
    except:
        warnings.warn("Connection Timeout, waiting 1 minute to retry..")
        time.sleep(10)
        return responce_manager(url, headers)



BASE = "http://ddbonline.ddbst.com/DDBSearch/onlineddboverview.exe?submit="
TYPE_OVERVIEW = "Overview&"
TYPE_DETAILS = "Details&"
COMPLIST = "systemcomplist="

Name = ""

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}


dataDict = {}
mixData = {}
tempDict = {}


SQLcon = sqlite3.connect('./DDBST_Meta.db')
SQLCursor = SQLcon.cursor()


DDB_RN_Sequences = SQLCursor.execute('SELECT DISTINCT DDB_RN_Sequence FROM Mixure_Property_Metadata;')

CompleteReg = []
for tuple_i in  DDB_RN_Sequences.fetchall():
    Splitted_Regs = tuple_i[0].split(',')
    Splitted_Regs = [int(item) for item in Splitted_Regs ]
    
    for number in Splitted_Regs:
        if number not in CompleteReg:
            CompleteReg.append(number)

CompleteReg.sort()


DDB_RN_reg = SQLCursor.execute('SELECT DDB_RN FROM Component_Registry;')
Registered_DDBs = []
for tuple_i in  DDB_RN_reg.fetchall():
    Registered_DDBs.append(tuple_i[0])

missingDDBS = []

for number in CompleteReg:
    if number not in Registered_DDBs:
        missingDDBS.append(number)





for DDBSTIndexNum in tqdm(missingDDBS):
    responce = responce_manager(BASE + TYPE_OVERVIEW + COMPLIST + str(DDBSTIndexNum), headers=header )
    #HTML_cont = httplib.parser.fromstring(responce.content.decode("utf-8"))
    soup = BeautifulSoup(responce.text, 'html.parser')
    chemEntryName = soup.findAll('tr')[4].findAll('td')[1].text
    if chemEntryName == "" or chemEntryName == "Reserved Entry" or DDBSTIndexNum >= 1 +1:
        break # break while
    
    # assuming the entry is valid.. add cas and formula entries
    tempDict.update({ soup.findAll('tr')[3].findAll('th')[1].text : chemEntryName } )
    tempDict.update({ soup.findAll('tr')[3].findAll('th')[2].text : soup.findAll('tr')[4].findAll('td')[2].text })
    tempDict.update({ soup.findAll('tr')[3].findAll('th')[3].text : soup.findAll('tr')[4].findAll('td')[3].text })
    
    # See detail page, if !"No data available for this component.", then add data entires for pure component props.
    responce = responce_manager(BASE + TYPE_DETAILS + COMPLIST + str(DDBSTIndexNum), headers=header )
    soupPurePropDetails = BeautifulSoup(responce.text, 'html.parser')
    
    tempPPdict = {}
    if re.search('No data available for this component.', soupPurePropDetails.text) == None: # i.e. data exsits for the pure properties
        Table_Headers = ['Property','Points','Sets','Temperature Range', 'States', 'Sets']
        PropertyType = ''
        propDict = {}
        statesetDict = {}
        for entry in  soupPurePropDetails.find_all('tr')[6:-3]:
            entryItems = entry.findAll('td')
            
            if entryItems[0].text != '':
                if PropertyType != '':
                    propDict.update({'State Sets' : statesetDict })
                    tempPPdict.update({PropertyType : propDict})
                propDict = {}
                statesetDict = {}
                PropertyType = entryItems[0].text
            
            if entryItems[1].text != '':
                propDict.update({'Points' : entryItems[1].text})
            if entryItems[2].text != '':
                propDict.update({'Sets' : entryItems[2].text})
            if entryItems[3].text != '':
                propDict.update( {'Temperature Range' : entryItems[3].text})
            if entryItems[4].text != '':
                statesetDict.update({entryItems[4].text : entryItems[5].text })
                
            
        propDict.update({'State Sets' : statesetDict })
        tempPPdict.update({PropertyType : propDict}) # last element
        
        tempDict.update({'Pure Component Data' : tempPPdict})
        
        # push pure component data to the sqlite db:
        for key in tempPPdict.keys():
            StatesOfPurePropString = ''
            for stateSet in tempPPdict[key]['State Sets'].keys():
                StatesOfPurePropString += stateSet +'_' + tempPPdict[key]['State Sets'][stateSet] + ';'
            
            StatesOfPurePropString = StatesOfPurePropString[:-1]
            
            
            SetsSQLWrite = ''
            try:
                SetsSQLWrite =  tempPPdict[key]['Sets']
            except:
                SetsSQLWrite = ''
            PointsSQLWrite = ''
            try:
                PointsSQLWrite = tempPPdict[key]['Points']
            except:
                PointsSQLWrite = ''
            TempRangeSQLWrite = ''
            try:
                TempRangeSQLWrite = tempPPdict[key]['Temperature Range'].strip('(').strip(')')
            except:
                TempRangeSQLWrite = ''
            
            
            SQLCursor.execute('INSERT INTO Pure_Property_Metadata VALUES (' + \
                            str(DDBSTIndexNum) + ','+ \
                            '\'' + key + '\',' + \
                            '\'' + PointsSQLWrite + '\',' +  \
                            '\'' + SetsSQLWrite + '\',' + \
                            '\'' + TempRangeSQLWrite +  '\',' + \
                            '\'' + StatesOfPurePropString + '\')' )
    
    # push stuff to the sql db; component number and formula                
    SQLCursor.execute('INSERT INTO Component_Registry VALUES (' + \
                   str(DDBSTIndexNum) + ','+ \
                   '\'' + chemEntryName + '\',' + \
                   '\'' + tempDict['CAS-RN'] + '\',' + \
                   '\'' + tempDict['Formula'] + '\')' )
    
    SQLcon.commit()
    
    
    
    ### Section for mixure data ###
    ###MixSections = soup.findAll('tr')[3]
    # add thing to mixDataif first no. is DDBSTIndexNum:
    mixEntryTables = soup.findAll('tr')[7:-4]
    for TableEntries in mixEntryTables:
        LineInformation = TableEntries.findAll('td')
        if len( LineInformation ) > 0:
            LineSplitted = str(LineInformation[1]).split('<br/>')
            FirstComp = BeautifulSoup(LineSplitted[0], 'html.parser').text
            if FirstComp == str(DDBSTIndexNum):
                responceDetailPage = responce_manager( LineInformation[-1].find('a').get_attribute_list('href')[0], headers=header)
                DetailSoup = BeautifulSoup(responceDetailPage.text, 'html.parser')
                
                Detail_tables = DetailSoup.findAll('table')[3:5]
                tempDetailDict = {}
                
                dataSeriesName = ''
                for line in  Detail_tables[0].findAll('tr')[1:]:
                    dataSeriesName += line.find('td').text + ','
                dataSeriesName = dataSeriesName[:-1] # remove the last comma
                
                for line in Detail_tables[1].findAll('tr')[1:-1]:
                    lineEntries =  line.findAll('td')
                    if len(lineEntries) == 6 and  re.search('[a-zA-Z]{2}', lineEntries[0].text.strip('\r').strip('\n') ) != None and  lineEntries[0].text.strip('\r').strip('\n')  != "Total":
                        tempDetailDict.update( { lineEntries[0].text.strip('\r').strip('\n') : \
                                            { "Sets" : lineEntries[2].text, \
                                             "Points" : lineEntries[3].text,  \
                                            "Temperature Range" : lineEntries[4].text, \
                                                "Pressure Range" : lineEntries[5].text
                                                 }  } )
                #mixData.update({dataSeriesName : tempDetailDict})
                
                # push mix data to sql-db 
                for key in tempDetailDict.keys():
                    SQLCursor.execute('INSERT INTO  Mixure_Property_Metadata VALUES (' + \
                                    '\'' + dataSeriesName  + '\',' + \
                                    '\'' + key + '\',' + \
                                    '\'' + tempDetailDict[key]['Sets'] + '\',' + \
                                    '\'' + tempDetailDict[key]['Points'] + '\',' + \
                                    '\'' + tempDetailDict[key]['Temperature Range'] + '\',' + \
                                    '\'' + tempDetailDict[key]['Pressure Range']  + '\')' )
                SQLcon.commit()
                
                
    
    
    # preparte for next entry:
    #dataDict.update( {DDBSTIndexNum : tempDict} )
    tempDict = {}


SQLcon.close()

#dataDict.update({ "Mixure Data" : mixData } ) 


#fp = open('./MetaData.json', mode='w')
#fp.write(json.dumps(dataDict, indent=4) )
#fp.close()