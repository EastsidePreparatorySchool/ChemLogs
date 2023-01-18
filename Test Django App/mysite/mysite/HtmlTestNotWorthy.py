import requests
from bs4 import BeautifulSoup
url1 = "https://www.flinnsci.com/sds_431-lauric-acid/sds_431/"
def Aroura_Great():
    headers =  {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    url1 = "http://www.flinnsci.com/sds_207-calcium-sulfate-dihydrate/sds_207/"
    r = requests.get(url1, headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    tables = soup.find_all("div", {"class": "sds-document_section-content"})
    print(tables)

Aroura_Great()


#<div class="first-section">
#<h3>Lauric Acid</h3>
 #                                       Flinn Scientific, Inc.  P.O. Box 219,  Batavia, IL  60510  (800) 452-1261<br/>Chemtrec 
#Emergency Phone Number: (800) 424-9906
#                                    </div>


# <td>143-07-7</td>

#<table class="table component-table">