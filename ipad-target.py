#!/usr/bin/python

import urllib
import urllib2
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import sys

import json as json

mode = sys.argv[1]
zip = sys.argv[2]
dpcis = sys.argv[3:]

models = {
    # Currently sold in stores
    '057-10-0172': 'Apple iPad mini 16GB Wi-Fi - Black (MD528LL/A)',
    '057-10-0173': 'Apple iPad mini 16GB Wi-Fi - White (MD531LL/A)',
    '057-10-0174': 'Apple iPad mini 32GB Wi-Fi - Black (MD529LL/A)',
    '057-10-0175': 'Apple iPad mini 32GB Wi-Fi - White (MD532LL/A)',
    '057-10-1830': 'Apple 16GB iPad 2 with Wi-Fi - Black (MC954LL/A)',
    '057-10-1839': 'Apple 16GB iPad 2 with Wi-Fi - White (MC989LL/A)',
    '057-10-2024': 'Apple 64GB iPad with Wi-Fi (3rd generation) - Black (MC707LL/A)',
    '057-10-2026': 'Apple 16GB iPad with Wi-Fi (3rd generation) + 4G for AT&T - Black (MD366LL/A)',
    '057-10-2031': 'Apple 64GB iPad with Wi-Fi (3rd generation) + 4G for AT&T - White (MD371LL/A)',
    '057-10-2053': 'Apple 32GB iPad with Retina display - White (MD514LL/A)',
    '057-10-2054': 'Apple 64GB iPad with Retina display - Black (MD512LL/A)',
    '057-10-2055': 'Apple 64GB iPad with Retina display - White (MD515LL/A)',

    # Not sold in stores (not an exhaustive list)
    '057-10-2020': 'Apple 16GB iPad with Wi-Fi (3rd generation) - Black (MC705LL/A)',
    '057-10-2021': 'Apple 16GB iPad with Wi-Fi (3rd generation) - White (MD328LL/A)',
    '057-10-2022': 'Apple 32GB iPad with Wi-Fi (3rd generation) - Black (MC706LL/A)',
    '057-10-2023': 'Apple 32GB iPad with Wi-Fi (3rd generation) - White (MD329LL/A)',
    '057-10-2025': 'Apple 64GB iPad with Wi-Fi (3rd generation) - White (MD330LL/A)',
    '057-10-2027': 'Apple 16GB iPad with Wi-Fi (3rd generation) + 4G for AT&T - White (MD369LL/A)',
    '057-10-2028': 'Apple 32GB iPad with Wi-Fi (3rd generation) + 4G for AT&T - Black (MD367LL/A)',
    '057-10-2029': 'Apple 32GB iPad with Wi-Fi (3rd generation) + 4G for AT&T - White (MD370LL/A)',
    '057-10-2030': 'Apple 64GB iPad with Wi-Fi (3rd generation) + 4G for AT&T - Black (MD368LL/A)',
    '057-10-2032': 'Apple 16GB iPad with Wi-Fi (3rd generation) + 4G for Verizon - Black (MC733LL/A)',
    '057-10-2033': 'Apple 16GB iPad with Wi-Fi (3rd generation) + 4G for Verizon - White (MD363LL/A)',
    '057-10-2034': 'Apple 32GB iPad with Wi-Fi (3rd generation) + 4G for Verizon - Black (MC744LL/A)',
    '057-10-2036': 'Apple 32GB iPad with Wi-Fi (3rd generation) + 4G for Verizon - White (MD364LL/A)',
    '057-10-2037': 'Apple 64GB iPad with Wi-Fi (3rd generation) + 4G for Verizon - Black (MC756LL/A)',
    '057-10-2038': 'Apple 64GB iPad with Wi-Fi (3rd generation) + 4G for Verizon - White (MD365LL/A)',

    '057-10-0183': 'Apple 32GB iPad with Retina display Wi-Fi + Cellular (AT&T) - Black (MD517LL/A)',
    '057-10-0184': 'Apple 32GB iPad with Retina display Wi-Fi + Cellular (Verizon - Black (MD523LL/A)',
    '057-10-0185': 'Apple 32GB iPad with Retina display Wi-Fi + Cellular (Sprint - Black (ME196LL/A)',
    '057-10-2050': 'Apple 16GB iPad with Retina display - Black (MD510LL/A)',
    '057-10-2051': 'Apple 16GB iPad with Retina display - White (MD513LL/A)',
    '057-10-2052': 'Apple 32GB iPad with Retina display - Black (MD511LL/A)',
    '241-27-2248': 'Apple 16GB iPad with Retina display Wi-Fi + Cellular (AT&T) - Black (MD516LL/A)',
    '241-27-2250': 'Apple 16GB iPad with Retina display Wi-Fi + Cellular (AT&T) - White (MD519LL/A)',
    '241-27-2256': 'Apple 32GB iPad with Retina display Wi-Fi + Cellular (Verizon)- White (MD526LL/A)',
    '241-27-2257': 'Apple 64GB iPad with Retina display Wi-Fi + Cellular (Verizon) - White (MD527LL/A)',
    '241-27-2259': 'Apple 64GB iPad with Retina display Wi-Fi + Cellular (Sprint)- Black (ME197LL/A)',
    '241-27-2263': 'Apple 32GB iPad with Retina display Wi-Fi + Cellular (AT&T) - White (MD520LL/A)',
    '241-27-4384': 'Apple 128GB iPad with Retina display - Black (ME392LL/A)',
    '241-27-4385': 'Apple 128GB iPad with Retina display - White (ME393LL/A)',

    '057-10-0176': 'Apple iPad mini 64GB Wi-Fi - Black (MD530LL/A)',
    '057-10-0177': 'Apple iPad mini 64GB Wi-Fi - White (MD533LL/A)',
    '057-10-0178': 'Apple iPad mini 16GB Wi-Fi + Cellular (AT&T) - Black (MD534LL/A)',
    '057-10-0180': 'Apple iPad mini 32GB Wi-Fi + Cellular (AT&T) - Black (MD535LL/A)',
    '057-10-0187': 'Apple iPad mini 32GB Wi-Fi + Cellular (Verizon) - White (MD544LL/A)',
    '057-10-0189': 'Apple iPad mini 64GB Wi-Fi + Cellular (Verizon) - White (MD545LL/A)',
    '241-27-2241': 'Apple iPad mini 32GB Wi-Fi + Cellular (AT&T) - White (MD538LL/A)',
    '241-27-2243': 'Apple iPad mini 16GB Wi-Fi + Cellular (Verizon) - Black (MD540LL/A)',
    '241-27-2244': 'Apple iPad mini 16GB Wi-Fi + Cellular (Verizon) - White (MD543LL/A)',
}

results = ""
stores = {}

if not dpcis:
    dpcis = models.keys()

jsonurl = 'http://api.target.com/products/v3/saleable_quantity_by_location?key=q0jGNkIyuqUTYIlzZKoCfK6ugaNGSP8h'

def getjsonurl():
    fiatsurl = 'http://www.target.com/FiatsCmd?'
    # Get a key to look stuff up with. Use any item get the current key.
    fiatsdata = urllib.urlencode({
	'template': 'medium',
	'overlayId': 'FindinStore',
	'pageType': 'pdp',
	'fiatLocation': 'product+detail',
	'catalogEntryID': '204704844',
	'partNumber': '14000303',
	'ValidDpci': '057-10-2020'
    })

    req = urllib2.Request(fiatsurl + fiatsdata, '', {'X-Requested-With': 'XMLHttpRequest'})
    response = urllib2.urlopen(req)
    #print response.info()
    page = response.read()

    soup = BeautifulSoup(page)

    jsonurl = soup.find('input', attrs={'id': 'saleableQtyLocURL'})['value']
    return jsonurl

def getproductjson(jsonurl):
	jsondata = json.dumps({
	    "products": [{
		"product_id": dpci,
		"desired_quantity": "1"
	    } for dpci in dpcis],
	    "nearby": zip,
	    "radius": "25",
	    "multichannel_options":[{
		"multichannel_option": "none"
	    }]
	})
	req = urllib2.Request(jsonurl, jsondata, {'Content-Type': 'application/json; charset=UTF-8', 'Accept': 'application/json'})
	response = urllib2.urlopen(req)
	page = response.read()
	return page

page = getproductjson(jsonurl)

products = json.loads(page)['products']

for product in products:
    product_id = product['product_id']
    # Look up friendly product name
    if product_id in models:
        product_name = models[product_id]
    else:
        product_name = product_id

    for store in product['stores']:
        if store['saleable_quantity'] > 0:
	    if product_name:
		results += "%s:\n" % (product_name,)
		product_name = None
            results += "    %s: %s (Qty: %d)\n" % (store['store_name'], store['availability_status'], store['saleable_quantity'])
            if store['store_id'] not in stores:
                stores[store['store_id']] = store
    results += '\n'

if stores:
    results += 'Store addresses:\n'
    for store in stores.itervalues():
        results += "    %s: %s\n" % (store['store_name'], store['store_address'])
    
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
 
