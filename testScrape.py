import urllib2
import requests 

import re
from bs4 import BeautifulSoup

import pdb

page_main = 'http://www.ddbst.com/free-data.html'
page_1 = 'http://www.ddbst.com/en/EED/PCP/CMPS_C3.php'
ex_DB = 'http://www.ddbst.com/en/EED/PCP/PCPindex.php'
base = 'http://www.ddbst.com/'
excessH_DB = 'http://www.ddbst.com/en/EED/HE/HEindex.php'


DB_multi_set = 'http://www.ddbst.com/en/EED/VLE/VLE%20Acetonitrile%3BAcetic%20acid.php'


def DDBST_table(DDBST_url):
    #page = urllib2.urlopen(DDBST_url)
    
    page = requests.get(DDBST_url).text
    
    soup = BeautifulSoup(page, 'html.parser')
    tab = []
    for rel_item in soup.find_all(['table','h3']):
        if re.search('Data Set',rel_item.get_text() ):
            tab.append(['$$$'+rel_item.get_text()] )
            
        elif rel_item.find_all('a'): # eliminates picture tables
            continue
        else:
            for line in rel_item.find_all('tr'):
                fetchline = []
                
                for elem in line.find_all(['th','td']):
                    # string without whitespace before of after characters
                    # added utf-8 formating to include unusual letters i.e. german letters ect..
                    item = elem.get_text().strip().encode('utf-8') 
                    
                    try:
                        fetchline.append(item)
                    except:
                        fetchline.append('PARSING_ERROR_HERE')
                        
                #print(fetchline)
                tab.append(fetchline)

    return tab

def DDBST_DB_free(prnt):
    page = urllib2.urlopen(page_main)
    soup = BeautifulSoup(page, 'html.parser')
    tab = soup.find_all('table')[0]
    res = ['url']
    for fline in tab.find_all('tr')[0].find_all('strong'):
        res.append(fline.get_text())

    res = [res] # first array done

    for line in tab.find_all('tr')[1:]:

        li = []
        for hlink in line.find_all('a'):
            li.append(hlink.get('href'))
        qlist = [li]

        for elem in line.find_all(['a','td','th']):
            qlist.append( elem.get_text() )

        res.append(qlist)
    # end for

    if prnt:
        for hline in res:
            print(hline)

    return res

def All_links(url):
    ''' fetches all possible urls from href tags'''
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    h = []
    for link in soup.find_all('a'):
        h.append(link.get('href'))
    return h

def DB(DDBST_url):
    ''' fetches all urls endings with databases in a specific main database Pure component properties 
    ect..'''
    page = requests.get(DDBST_url).text
    
    soup = BeautifulSoup(page, 'html.parser')
    
    
    all_par_iter = [m.start(0) for m in re.finditer('/', ex_DB)]
    base_url = DDBST_url[0:all_par_iter[-1]]
    
    
    
    ret_elem = []
    for link in soup.find_all('p')[3:-1]:
        #pdb.set_trace()
        header = link.find('a').get('href')
        name = link.find('a').getText()
        
        #wspace_iter = [m.start(0) for m in re.finditer(' ', header)]
        #if wspace_iter:
            # add %20 in space
            #header = header[0:wspace_iter[0]] + ' ' + header[wspace_iter[0]+1:]
        #pdb.set_trace()
        ret_elem.append([base_url + '/' + header, name])
        
        
        
    return ret_elem





