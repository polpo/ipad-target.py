#!/usr/bin/python

import urllib
import urllib2
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import sys

url = 'http://www.target.com/FiatsCmd?'

mode = sys.argv[1]
zip = sys.argv[2]
dpcis = sys.argv[3:]

models = {
    '057-10-2020': ('204704844','14000303','16GB The new iPad with Wi-Fi - Black (MC705LL/A)'),
    '057-10-2021': ('204704865','14000304','16GB The new iPad with Wi-Fi - White (MD328LL/A)'),
    '057-10-2022': ('204704833','13999147','32GB The new iPad with Wi-Fi - Black (MC706LL/A)'),
    '057-10-2023': ('204704858','13999148','32GB The new iPad with Wi-Fi - White (MD329LL/A)'),
    '057-10-2024': ('204704877','13999149','64GB The new iPad with Wi-Fi - Black (MC707LL/A)'),
    '057-10-2025': ('204704934','13999150','64GB The new iPad with Wi-Fi - White (MD330LL/A)'),
    '057-10-2026': ('204704892','13999151','16GB The new iPad with Wi-Fi + 4G for AT&T - Black (MD366LL/A)'),
    '057-10-2027': ('204704916','13999152','16GB The new iPad with Wi-Fi + 4G for AT&T - White (MD369LL/A)'),
    '057-10-2028': ('204704936','13999153','32GB The new iPad with Wi-Fi + 4G for AT&T - Black (MD367LL/A)'),
    '057-10-2029': ('204704924','13999154','32GB The new iPad with Wi-Fi + 4G for AT&T - White (MD370LL/A)'),
    '057-10-2030': ('204704940','13999155','64GB The new iPad with Wi-Fi + 4G for AT&T - Black (MD368LL/A)'),
    '057-10-2031': ('204704904','13999156','64GB The new iPad with Wi-Fi + 4G for AT&T - White (MD371LL/A)'),
    '057-10-2032': ('204704928','13999157','16GB The new iPad with Wi-Fi + 4G for Verizon - Black (MC733LL/A)'),
    '057-10-2033': ('204704943','13999158','16GB The new iPad with Wi-Fi + 4G for Verizon - White (MD363LL/A)'),
    '057-10-2034': ('204704906','13999159','32GB The new iPad with Wi-Fi + 4G for Verizon - Black (MC744LL/A)'),
    '057-10-2036': ('204785282','14038112','32GB The new iPad with Wi-Fi + 4G for Verizon - White (MD364LL/A)'),
    '057-10-2037': ('204785234','14038213','64GB The new iPad with Wi-Fi + 4G for Verizon - Black (MC756LL/A)'),
    '057-10-2038': ('204785257','14038214','64GB The new iPad with Wi-Fi + 4G for Verizon - White (MD365LL/A)'),
}

results = ""
stores = {}

if not dpcis:
    dpcis = models.keys()

for dpci in dpcis:
    data = urllib.urlencode({
        'partNumber': models[dpci][1],
        'catalogEntryID': models[dpci][0],
        'ValidDpci': dpci,
        'zipCode': zip,
        'isSoftRefresh': 'true',
        'attrName_1': '',
        'attrName_2': '',
        'city': '',
        'state': '',
    })

    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    #print response.info()
    page = response.read()

    soup = BeautifulSoup(page)

    trs = soup.find_all('tr')

    for tr in trs[2:]:
        tds = tr.find_all('td')
        store = tds[1].span.string
        address = tds[1].select('.store-address')[0].string
        status = tds[2].strong.string
        #print store, status

        if status not in ("out of stock", "not sold at this store"):
            results += models[dpci][2] + ': ' + store + ': ' + status + '\n'
            if store not in stores:
                stores[store] = address

if stores:
    results += "\nStore addresses:\n"
    for store in stores:
        results += store + ": " + ' '.join(stores[store].split()) + "\n"
    
if results:
    if mode == 'print':
        print results
    elif mode == 'email':
        msgto = ['me@example.com']
        msgfrom = 'me@example.com'
        msg = MIMEText(results)
        msg['Subject'] = 'iPad status'
        msg['To'] = ', '.join(msgto)
        msg['From'] = msgfrom

        s = smtplib.SMTP('localhost')
        s.sendmail(msgfrom, msgto, msg.as_string())
        s.quit()
 
