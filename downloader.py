
import os
import testScrape
import re
import time
import pdb

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
            createFile(ChemName+'_'+CAS_cur+'.tsv',dir_name,table,'\t')
            if verbose:
                print 'Pure component propeties downloaded: ' + ChemName + ' CAS: ' + CAS_cur 
                print 'Compnent #' + str(subsNum) + ' of ' + Head[1][-1]
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
    createFile(ChemName+'_'+CAS_cur+'.tsv',dir_name,table,'\t')
    
    #return table
    
def createFile(fileName, filePath, contentMat, sepStr):
    
    # Task 1: create relevant directories for the intended path
    
    dirSplit = re.split('/',filePath)
    lc = './'
    for loc in dirSplit:
        dirLst = os.walk(lc).next()[1]
        
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
                    fileStream.write(str(elem)+sepStr)
                except:
                    fileStream.write('SOME_ERROR_OCCOURED_HERE'+sepStr)
                    print 'createFile: error at wrinting file'   
            fileStream.write('\n')
    
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
            print 'Some error occured for url: ' + url + ' \n broken???'
            print 'Skipped ' + str(counter) + ' of ' + str(total_elems) + ' element'
            
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
        
        
        fileTitle += '.tsv'
        
        createFile(fileTitle, path, [content], '\t')
        
        if verbose:
            print 'Status of Database: ' + name
            print str(counter) + ' of ' + str(total_elems) + ' items downloaded'
        counter += 1
        #time.sleep(10)
        
        
def AllDB_dwnl(verbose):
     for line in Head[2:-1]:
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
    PCP_dwnld(verbose)
    AllDB_dwnl(verbose)
    print 'DDBST free database downloaded to ./DB'


if __name__ == '__main__':
    try:
        verbose = sys.argv[1]
    except:
        verbose = True    
        
    main(verbose)
    