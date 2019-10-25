
import os
import testScrape
import re
import time
import pdb
import json

Head = testScrape.DDBST_DB_free(0)



        

def PCP_dwnld(verbose):
    url_Index = testScrape.base + Head[1][0][0]
    DB_elems = testScrape.DB(url_Index)
    dir_name = 'DB/'+ Head[1][1]
    
    table_temp = []
    table = []
    CAS_cur = []; ChemName = []
    
    subsNum = 1
    
    for u in DB_elems:
        table_temp = testScrape.DDBST_table(u[0])
        CAS_n = table_temp[1][2]; Chem_n = table_temp[1][3]
        
        contentTitle = '$$$' + u[1]
        
        if not ChemName:
            CAS_cur = CAS_n; ChemName = Chem_n
            if table == []:
                
                table = [table_temp[:2]]
                table.append([[contentTitle]])
                table.append(table_temp[2:])
                
                
            else:
                table.append(table_temp)
                
        elif ChemName != Chem_n:
            
            createFile(str(ChemName)+'_'+str(CAS_cur)+'.tsv',dir_name,table,'\t')
            createJsonFile(str(ChemName)+'_'+str(CAS_cur)+'.json',dir_name,table )
            if verbose:
                print ('Pure component propeties downloaded: ' + str(ChemName) + '; CAS: ' + str(CAS_cur)  )
                print ('Compnent #' + str(subsNum) + ' of ' + str(Head[1][-1] ))
            subsNum += 1
            
            
            table = [table_temp[:2]]
            table.append([[contentTitle]])
            table.append(table_temp[2:])
            CAS_cur = CAS_n; ChemName = Chem_n
            
        elif ChemName == Chem_n:
            table.append([[contentTitle]])
            table.append(table_temp[2:])
        else:
            continue
    
    # save the last entry
    createFile(str(ChemName)+'_'+str(CAS_cur)+'.tsv',dir_name,table,'\t')
    createJsonFile(str(ChemName)+'_'+str(CAS_cur)+'.json',dir_name,table)
    #return table
    
def createFile(fileName, filePath, contentMat, sepStr):
    
    # Task 1: create relevant directories for the intended path
    
    dirSplit = re.split('/',filePath)
    lc = './'
    for loc in dirSplit:
        os.walk(lc)
        dirLst = os.walk(lc).send(None)[1]
        
        pathExsits = False
        
        for actDirs in dirLst:
            if actDirs == loc:
                pathExsits = True # path exsits
            else:
                continue
            
        if pathExsits:
            lc += loc +'/'
        #elif pathExsits == False:
        else:
            lc += loc + '/'
            try:
                os.mkdir(lc)
            except:
                #print 'directory exists!'
                #print 'loc = ' + loc
                #print 'actDirs = ' + actDirs + '\n\n'
                []
                
                
    # Task 2: write the file to the given path 
    
    fileStream = open(filePath + '/' + fileName, 'w')
    for q in contentMat:
        for line in q:
            for elem in line:
                try:
                    if elem == line[-1]:
                        fileStream.write(str(elem))
                    else:
                        fileStream.write(str(elem)+sepStr)
                        
                except:
                    fileStream.write('SOME_ERROR_OCCOURED_HERE'+sepStr)
                    print ('createFile: error at writing file'   )
            fileStream.write('\n')
    
    fileStream.close()
    
def createJsonFile(fileName, filePath, contentMat):
        # Task 1: create relevant directories for the intended path
    
    dirSplit = re.split('/',filePath)
    lc = './'
    for loc in dirSplit:
        os.walk(lc)
        dirLst = os.walk(lc).send(None)[1]
        
        pathExsits = False
        
        for actDirs in dirLst:
            if actDirs == loc:
                pathExsits = True # path exsits
            else:
                continue
            
        if pathExsits:
            lc += loc +'/'
        #elif pathExsits == False:
        else:
            lc += loc + '/'
            try:
                os.mkdir(lc)
            except:
                #print 'directory exists!'
                #print 'loc = ' + loc
                #print 'actDirs = ' + actDirs + '\n\n'
                []
    # Task 2 : export json structure to file
    fileStream = open(filePath + '/' + fileName, 'w')
    json_dict = {}
    l = 1
    
    if (contentMat[0][0][0] == 'Formula'): # i.e. pure substance data
        for i in range(len(contentMat[0][0])):
            json_dict.update({contentMat[0][0][i]: contentMat[0][1][i] })
        
        for j in range (len(contentMat)):
            temp_keys = []
            temp_values = []
            if (contentMat[j][0][0][0:3] == '$$$'):
                main_key = contentMat[j][0][0][3:]
                for k in range(len(contentMat[j+1][0])):
                    temp_keys.append( contentMat[j+1][0][k])
                    temp_values.append([])
                    l = 1
                    while (contentMat[j+1][l][0] != 'Number'):
                        temp_values[k].append( contentMat[j+1][l][k] )
                        l += 1
                    
                # find the references...
                temp_keys.append('Reference')
                temp_values.append([])
                for p in range(l+1, len(contentMat[j+1])):
                    temp_values[-1].append([contentMat[j+1][p][0], contentMat[j+1][p][1] ])
                    
                        
                temp_dict  = {}
                for u in range(len(temp_keys)):
                    temp_dict.update({ temp_keys[u] : temp_values[u] })
                json_dict.update({main_key: temp_dict})
                
            else:
                continue
            
                
                
        
    elif (contentMat[0][0][0][0:3] == '$$$' ): # i.e. we have mixture data
        ## copy pased code :::
        temp_keys = []
        temp_values = []
        temp_dict = {}
        temp_dict2 = {}
        i = 0
        DatasetName_index = []
        Component_header_index = []
        Component_index = []
        Constants_index = []
        Table_head_index = []
        Table_data_index = []
        Author_index = []
        #Constant_regex_pat = re.compile('[a-zA-Z]+')
        #Table_head_regpat = re.compile('[a-z]{1, 99}\[[a-z]{1, 99}\]')
#        while ( i < len(contentMat[0])):
#            if (contentMat[0][i][0][:3] == '$$$'):
#                main_key = contentMat[0][0][0][3:]
#                i += 1
#            elif (contentMat[0][i][0] == 'No.'):
#                for j in range(len(contentMat[0][i])):
#                    k=i + 1
#                    temp_keys.append(  contentMat[0][i][j])
#                    temp_values
#                    try:
#                        while ( k < len(contentMat[0]) and int ( contentMat[0][k][0] ) > 0 ):
#                            temp_values.append(contentMat[0][k][j])
#                            k += 1
#                    except:
#                        ## component list is finished...
#                        
#                        temp_dict.update({temp_keys[0] : temp_values})
#                        
#                        temp_keys = []
#                        temp_values = []
#                        #while ( k < len(contentMat[0]) and int ( contentMat[0][k][0] ) ):
#                temp_dict2.update({'Components' : temp_dict })
                ## extract constant values:
        
        dataset_key = ''
        dataset = {}
        Source_set = []
        
        Num_datadict = {}
        Num_datadict_keys = []
        Num_datadict_values = []
        
        Mix_params_dict = {}
        Mix_params_keys = []
        Mix_params_values = []
        
        const_dict = {}
        const_keys = []
        const_values = []
        
        
        data_set_name = ''

        
        for i in range(len(contentMat)):
            for j in range(len(contentMat[i])):
                if ( contentMat[i][j][0][0:3] == '$$$'): # find the title of the dataset
                    DatasetName_index.append([i, j])
                    
                    
                    if ( j > 0 or i > 0):
                        # update the json dict of previous data
                        for k in range(len(Mix_params_keys)):
                            Mix_params_dict.update({Mix_params_keys[k] : Mix_params_values[k] })
                            
                        for k in range(len(const_keys)):
                            const_dict.update({const_keys[k]: const_values[k]})
                        
                        for k in range(len(Num_datadict_keys)):
                            Num_datadict.update({Num_datadict_keys[k] : Num_datadict_values[k] })
                        
                        if (len(Num_datadict_keys) < 0.1):
                            print("no datadict keys!")
                        
                        
                        dataset.update({"Constants": const_dict})
                        dataset.update({"Components": Mix_params_dict})
                        dataset.update({"Table": Num_datadict })
                        dataset.update({'Source' : Source_set})
                        
                        
                        json_dict.update({data_set_name : dataset})
                        
                        # rinse and repeat :)
                        dataset = {}
                        Num_datadict = {}
                        Num_datadict_keys = []
                        Num_datadict_values = []
        
                        Mix_params_dict = {}
                        Mix_params_keys = []
                        Mix_params_values = []
        
                        const_dict = {}
                        const_keys = []
                        const_values = []
                        
                        
                        
                        
                        
                        data_set_name = contentMat[i][j][0][3:]
                    
                    else:
                        data_set_name = contentMat[i][j][0][3:]
                        
                    
                elif(contentMat[i][j][0] == 'No.' and re.match( '\d{1,3}', contentMat[i][j+1][0] ) ): # find header of the component list
                    Component_header_index.append([i, j])
                    for k in range( len( contentMat[i][j])):
                        Mix_params_values.append([])
                        Mix_params_keys.append(contentMat[i][j][k])
                elif( len( contentMat[i][j]) == 5 and re.match('^[a-zA-Z]', contentMat[i][j][1] ) and not re.match('^[a-zA-Z]{1,4}\d{0,2} \[.*?\]$', contentMat[i][j][0] )  ): # find component list entries
                    if(  re.match('^\d', contentMat[i][j][2] ) and re.match('^\d{1,5}-\d{1,5}-\d{1,5}$', contentMat[i][j][3] )  ):
                        Component_index.append([i, j])
                        #Mix_params_keys.append(contentMat[i][j][0])
                        for k in range( len( contentMat[i][j])):
                            Mix_params_values[k].append(contentMat[i][j][k])
                                
                        
                        
                        
                        
                elif ( re.match( '^[a-zA-Z]{4,99}', contentMat[i][j][0] )  and  len(contentMat[i][j]) == 3 and  re.match( '^\d{0,99}.\d{0,99}', contentMat[i][j][1] )  and not re.match("\[", contentMat[i][j][0]) and contentMat[i][j][0] != 'Excess Volume [cm3/mol]' and contentMat[i][j][0] != 'Density [g/cm3]'  ): # find contant value for the dataset:
                    if contentMat[i][j][1] != '<empty>':
                        #Constants_index.append([i, j])
                        const_keys.append(contentMat[i][j][0])
                        const_values.append(contentMat[i][j][1:])
                        
                elif ( re.match('[a-zA-Z]{1,25}\d{0,2} \[.*?\]$', contentMat[i][j][0] ) or contentMat[i][j][0] == 'Excess Heat Capacity [J/mol*K]' or contentMat[i][j][0] == 'Heat Capacity [J/mol*K]' or contentMat[i][j][0] == 'Excess Volume [cm3/mol]' or contentMat[i][j][0] == 'Excess Volume [cm3/mol]'   ): #elif ( re.match( '^[a-zA-Z]{0,99} \[[a-zA-Z]{0,99}\]$'  , contentMat[i][j][0] ) ): # find table heading
                    # the table headings
                    Table_head_index.append([i, j])
                    for k in range(len(contentMat[i][j])):
                        Num_datadict_keys.append(contentMat[i][j][k])
                        #Num_datadict.update({Num_datadict_keys , []})
                        Num_datadict_values.append([])
                elif ( len(contentMat[i][j]) == len(Num_datadict_keys) and not re.match('^Source$'  , contentMat[i][j][0]) ): #elif ( re.match( '^\d{0,9}.\d{0,9}$'  , contentMat[i][j][0] )  or  contentMat[i][j][0] == '^<empty>' ): # find numerical table entries
                    Table_data_index.append([i, j])
                    for k in range(len(Num_datadict_keys)):
                        #Num_datadict.update({ Num_datadict_keys[k] : Num_datadict[  Num_datadict_keys[k]  ].append(contentMat[i][j][k]) } )
                        Num_datadict_values[k].append(contentMat[i][j][k])
                elif (re.match('^Source$'  , contentMat[i][j][0]) ):
                    Author_index.append([i, j])
                elif (re.match('^[a-zA-Z]{1,999999}', contentMat[i][j][0]) and len(contentMat[i][j][0]) > 23 ):
                    Source_set.append(contentMat[i][j][0])
                    
    
        # save the last entries
        for k in range(len(Mix_params_keys)):
            Mix_params_dict.update({Mix_params_keys[k] : Mix_params_values[k] })
                            
        for k in range(len(const_keys)):
            const_dict.update({const_keys[k]: const_values[k]})
                        
        for k in range(len(Num_datadict_keys)):
            Num_datadict.update({Num_datadict_keys[k] : Num_datadict_values[k] })
            
        if (len(Num_datadict_keys) < 0.1):
            print("no datadict keys!")
        #if (len(Num_datadict_values[0]) < 0.1):
        #    print("no values??")
                        
        dataset.update({"Constants": const_dict})
        dataset.update({"Components": Mix_params_dict})
        dataset.update({"Table": Num_datadict })
        dataset.update({'Source' : Source_set})
        
                        
                        
        json_dict.update({data_set_name : dataset})
                        
    elif (contentMat[0][0][0][0:3] == 'No.' ): # i.e. we have mixture data
        ## copy pased code :::
        temp_keys = []
        temp_values = []
        temp_dict = {}
        temp_dict2 = {}
        i = 0
        DatasetName_index = []
        Component_header_index = []
        Component_index = []
        Constants_index = []
        Table_head_index = []
        Table_data_index = []
        Author_index = []
        
        dataset_key = ''
        dataset = {}
        Source_set = []
        
        Num_datadict = {}
        Num_datadict_keys = []
        Num_datadict_values = []
        
        Mix_params_dict = {}
        Mix_params_keys = []
        Mix_params_values = []
        
        const_dict = {}
        const_keys = []
        const_values = []
        
        
        data_set_name = ''

        
        for i in range(len(contentMat)):
            for j in range(len(contentMat[i])):
                if(contentMat[i][j][0] == 'No.' and re.match( '\d{1,3}', contentMat[i][j+1][0] ) ): # find header of the component list
                    Component_header_index.append([i, j])
                    for k in range( len( contentMat[i][j])):
                        Mix_params_values.append([])
                        Mix_params_keys.append(contentMat[i][j][k])
                elif( len( contentMat[i][j]) == 5 and re.match('^[a-zA-Z]', contentMat[i][j][1] ) and not re.match('^[a-zA-Z]{1,4}\d{0,2} \[.*?\]$', contentMat[i][j][0] )  ): # find component list entries
                    if(  re.match('^\d', contentMat[i][j][2] ) and re.match('^\d{1,5}-\d{1,5}-\d{1,5}$', contentMat[i][j][3] )  ):
                        Component_index.append([i, j])
                        #Mix_params_keys.append(contentMat[i][j][0])
                        for k in range( len( contentMat[i][j])):
                            Mix_params_values[k].append(contentMat[i][j][k])
                                
                        
                        
                        
                        
                elif ( re.match( '^[a-zA-Z]{4,99}', contentMat[i][j][0] )  and  len(contentMat[i][j]) == 3 and  re.match( '^\d{0,99}.\d{0,99}', contentMat[i][j][1] )   ): # find contant value for the dataset:
                    if contentMat[i][j][1] != '<empty>':
                        #Constants_index.append([i, j])
                        const_keys.append(contentMat[i][j][0])
                        const_values.append(contentMat[i][j][1:])
                        
                elif ( re.match('^[a-zA-Z]{1,90}\d{0,2} \[.*?\]$', contentMat[i][j][0] ) or contentMat[i][j][0] == "Azeotropic Type"  ): #elif ( re.match( '^[a-zA-Z]{0,99} \[[a-zA-Z]{0,99}\]$'  , contentMat[i][j][0] ) ): # find table heading
                    # the table headings
                    Table_head_index.append([i, j])
                    for k in range(len(contentMat[i][j])):
                        Num_datadict_keys.append(contentMat[i][j][k])
                        #Num_datadict.update({Num_datadict_keys , []})
                        Num_datadict_values.append([])
                elif ( len(contentMat[i][j]) == len(Num_datadict_keys) and not re.match('^Source$'  , contentMat[i][j][0]) ): #elif ( re.match( '^\d{0,9}.\d{0,9}$'  , contentMat[i][j][0] )  or  contentMat[i][j][0] == '^<empty>' ): # find numerical table entries
                    Table_data_index.append([i, j])
                    for k in range(len(Num_datadict_keys)):
                        #Num_datadict.update({ Num_datadict_keys[k] : Num_datadict[  Num_datadict_keys[k]  ].append(contentMat[i][j][k]) } )
                        Num_datadict_values[k].append(contentMat[i][j][k])
                elif (re.match('^Source$'  , contentMat[i][j][0]) ):
                    Author_index.append([i, j])
                elif (re.match('^[a-zA-Z]{1,999999}', contentMat[i][j][0]) and len(contentMat[i][j][0]) > 23 ):
                    Source_set.append(contentMat[i][j][0])
                    
    
        # save the last entries
        for k in range(len(Mix_params_keys)):
            Mix_params_dict.update({Mix_params_keys[k] : Mix_params_values[k] })
                            
        for k in range(len(const_keys)):
            const_dict.update({const_keys[k]: const_values[k]})
                        
        for k in range(len(Num_datadict_keys)):
            Num_datadict.update({Num_datadict_keys[k] : Num_datadict_values[k] })
            
        if (len(Num_datadict_keys) < 0.1):
            print("no datadict keys!")
        #if (len(Num_datadict_values[0]) < 0.1):
        #    print("no values??")
                        
        dataset.update({"Constants": const_dict})
        dataset.update({"Components": Mix_params_dict})
        dataset.update({"Table": Num_datadict })
        dataset.update({'Source' : Source_set})
                        
                        
        json_dict = dataset
            
            
        
        
    #json.load
    #json.
    #json.dump(json_dict, fileStream)
    fileStream.write(json.dumps(json_dict, indent=4, sort_keys=True) )
    
    
    fileStream.close()

def mixPropDB_dwnld(url, name, verbose):
    DB_elems = testScrape.DB(url)
    path = './DB/'+name
    
    DB_elems = slimDB(DB_elems)
    
    counter = 1; total_elems = len(DB_elems)
    
    
    for element in DB_elems:
        url = element[0]
        
        try:
            content = testScrape.DDBST_table(url)
        except:
            print ('Some error occured for url: ' + url + ' \n broken???')
            print ('Skipped ' + str(counter) + ' of ' + str(total_elems) + ' element')
            
            counter += 1
            continue
        
        
        fileTitle = ''
        
        inter = 0
        while True:
            try:
                if content[inter] == ['No.', 'Formula', 'Molar Mass', 'CAS Registry Number', 'Name']:
                    break
            except:
                pdb.set_trace()
            inter += 1
        
        while re.match('\d',content[inter+1][0]):
            fileTitle += content[inter+1][-1] + '_'
            inter += 1
        
        
        createFile(fileTitle + '.tsv', path, [content], '\t')
        createJsonFile(fileTitle + '.json', path, [content])
        
        if verbose:
            print ('Status of Database: ' + name)
            print (str(counter) + ' of ' + str(total_elems) + ' items downloaded')
        counter += 1
        #time.sleep(10)
        
        
def AllDB_dwnl(verbose):
     for line in Head[2:-1]:#Head[2:-1]:
        urlIndex = line[0]; curDir = line[1]
        if len(urlIndex) == 2:
            DB_names = [line[2], line[3]]
        elif len(urlIndex) == 1:
            DB_names = [line[2]]
        
        for i in range(0,len(urlIndex)):
            urlIndex[i] = testScrape.base + urlIndex[i]
            
            mixPropDB_dwnld(urlIndex[i], DB_names[i],verbose)
            
        
        #print DB_names
        #print urlIndex

def slimDB(DBelements):
    uniqueElems = []
    for elem in DBelements:
        add = True
        for uniqe in uniqueElems:
            if elem[0] == uniqe[0]:
                add = False
            else:
                continue
        if add:
            uniqueElems.append(elem)
        else:
            continue
        
    return uniqueElems

        
def main(verbose):
    #PCP_dwnld(verbose)
    AllDB_dwnl(verbose)
    print ('DDBST free database downloaded to ./DB')


if __name__ == '__main__':
    try:
        verbose = sys.argv[1]
    except:
        verbose = True    
        
    main(verbose)
    
