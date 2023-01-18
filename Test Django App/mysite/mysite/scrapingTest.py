"""source:
https://levelup.gitconnected.com/scrap-data-from-website-and-pdf-document-for-django-app-fa8f37010085
"""

import requests
from bs4 import BeautifulSoup
url1 = "https://www.flinnsci.com/sds_431-lauric-acid/sds_431/"
def Aroura_Great(url, keyword, tag_, class_):
    headers =  {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    if (class_ == None):
        tables = soup.find_all(tag_)
    else:
        tables = soup.find_all(tag_, {"class": class_}) # this includes the 'safety' info
    Exclusion_Counter = 0
    for d in tables:
        divs = d.find_all("div")
        for div in divs:
            # print(type(div))
            if (str(div).__contains__(keyword)):
                # print(div)
                newStr = Toaster_Cool_and_Cadence(div)
            else:
                Exclusion_Counter += 1 
    print(Exclusion_Counter)

def Toaster_Cool_and_Cadence(to_filter):
    split_div = str(to_filter).split("\n")
    for line in split_div:
        line_final = str("")
        by_end = line.split(">")
        for l in by_end:
            line_final = line_final + l.split("<")[0]

    print(line_final)
    # print(split_div[1].strip())
    print('\n\n')
        
        #DivSections.append(div)
        #letters = set('qasd')
        #for word in DivSections:
            #if word in letters:
                #print (word)
        #if "Hazard" in div:
            #print(div)
    
#print("\n\n\n" + len(tables))
#print(str(soup))

def Cadence_Amazing():
    print("The other stuff")
    headers =  {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    tables = soup.find_all("div", {"class": "sds-document_section-content"})





# Aroura_Great(url1, "fifth", "div", "sds-document_section-content")
Aroura_Great(url1, "table", "div", "sds-document_section-content")

