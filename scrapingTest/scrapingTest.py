"""source:
https://levelup.gitconnected.com/scrap-data-from-website-and-pdf-document-for-django-app-fa8f37010085
"""

import requests
from bs4 import BeautifulSoup
headers =  {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
url = "https://www.flinnsci.com/sds_431-lauric-acid/sds_431/"
r = requests.get(url, headers=headers)
c = r.content
soup = BeautifulSoup(c, "html.parser")
# tables = soup.find_all("div", {"class": "sds-document_section-content"}) # this includes the 'safety' info
# for d in tables:
#     print(d)
# print("\n\n\n" + len(tables))
print(soup)