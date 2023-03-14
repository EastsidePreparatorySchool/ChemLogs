"""source:
https://levelup.gitconnected.com/scrap-data-from-website-and-pdf-document-for-django-app-fa8f37010085
"""

import requests
from bs4 import BeautifulSoup
url1 = "https://www.flinnsci.com/sds_431-lauric-acid/sds_431/"
def Aroura_Great(url, keyword, tag_ = None, class_ = None):
    global inclusion_counter
    headers =  {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    # if (tag_ == None):
    #     if (str(c).__contains__("<title>")):
    #         c_important = "".join(str(c).split("<title>")[1:])
    #         c_lines = c_important.split("\n")
    #         for line in c_lines:
    #             print("\n")
    #             print(line)
    #     return

    if (class_ == None):
        items = soup.find_all(tag_)
    else:
        items = soup.find_all(tag_, {"class": class_}) # this includes the 'safety' info

    # how many things are not included
    exclusion_counter = 0
    inclusion_counter = 0

    # for each item with the tag
    for it in items:
        divs = it.find_all(tag_)
        for div in divs:
            #print(type(div))
            # change it back to it if bad
            if (str(div).__contains__(keyword)):
                # print(div)
                Toaster_Cool_and_Cadence(div)
                # print(it)
                inclusion_counter +=1
            else:
                exclusion_counter += 1
                inclusion_counter += 1
    print(exclusion_counter)
    print(inclusion_counter)
    print(inclusion_counter-exclusion_counter)

def Toaster_Cool_and_Cadence(to_filter):
    global inclusion_counter
    #split_div.remove("<class 'bs4.element.Tag'>")
    split_div = str(to_filter).split("\n")
    split_div.pop()
    number = len(split_div)
    real_number = number -1
    for i in range(real_number):
        split_div.pop(0)
    print(number)
    #res = [split_div[i] for i in range(len(split_div)) if i == split_div.index(split_div[i])]
    #[res.append(x) for x in split_div if x not in res]
    # print(str(to_filter))
    for line in split_div:
        #if line == "<class 'bs4.element.Tag'>":
           # line.replace("<class 'bs4.element.Tag'>", "")
           # inclusion_counter +=1
        line_final = str("")
        by_end = line.split(">")
        for l in by_end:
            line_final = line_final + l.split("<")[0]
       # line_final.replace("<class 'bs4.element.Tag'>", "")

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
Aroura_Great(url1, "SECTION 16")

