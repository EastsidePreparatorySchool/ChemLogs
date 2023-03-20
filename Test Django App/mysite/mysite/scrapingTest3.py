"""source:
https://levelup.gitconnected.com/scrap-data-from-website-and-pdf-document-for-django-app-fa8f37010085
"""

import requests
from bs4 import BeautifulSoup
url1 = "https://www.flinnsci.com/sds_431-lauric-acid/sds_431/"

# find all paragraphs that include the desired word
def findAllCases(url, search_key):
    headers =  {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    paragraphs = soup.find("div", {"class": "sds-document_section-header"})
    print(paragraphs)

# Aroura_Great(url1, "fifth", "div", "sds-document_section-content")
findAllCases(url1, "Hazard")