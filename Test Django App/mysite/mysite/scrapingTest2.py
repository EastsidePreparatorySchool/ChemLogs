"""source:
https://levelup.gitconnected.com/scrap-data-from-website-and-pdf-document-for-django-app-fa8f37010085
"""

example = "<div class=\"sds-docuasdfsdfasment_section-footer\"> <small>N.A. = Not available, not all health aspects <br> of this substance have been fully investigated.</small>"
keyword = "div"

if example.__contains__(keyword):
    line_final = str("")
    by_end = example.split(">")
    for l in by_end:
        line_final = line_final + l.split("<")[0]

    print(line_final)

'''
OLD CODE STARTS HERE

import requests
from bs4 import BeautifulSoup
url1 = "https://www.flinnsci.com/sds_431-lauric-acid/sds_431/"
def Aroura_Great(url, keyword):
    headers =  {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    tables = soup.find_all("div", {"class": "sds-document_section-content"}) # this includes the 'safety' info

    for d in tables:
        divs = d.find_all("div")
        for div in divs:
            # print(type(div))
            if (str(div).__contains__(keyword)):
                # print(div)
                split_div = str(div).split("\n")
                for line in split_div:
                    

                        print(line_final.strip())
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

Aroura_Great(url1, "fifth")

OLD CODE ENDS HERE
'''
