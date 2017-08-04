
# Web scraping interface test
# using Beautiful Soup on redfin.com

# Alec Myres
# August 2017

from bs4 import BeautifulSoup
import urllib, locale, requests, sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import pandas as pd
import numpy as np
import selenium, time
from selenium import webdriver

# Selenium/PhantomJS test
driver = webdriver.PhantomJS(executable_path =
         '/usr/local/bin/phantomjs-2.1.1-macosx/bin/phantomjs')
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
time.sleep(3)
print driver.find_element_by_id('content').text
driver.close()

# Add custom HTTP headers
zipcode = '84095'
url = 'https://www.redfin.com/zipcode/' + zipcode
session = requests.Session()
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
req = session.get(url, headers = headers)
soup = BeautifulSoup(req.text, "lxml")






# for price conversions to ints
#locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

# Get pages, count
p = soup.find_all('ul', class_ = 'pager')[0]
p = p.contents[1]
pStr = p.a.string
pFirst = int(pStr.split(' ')[1])
pLast  = int(pStr.split(' ')[3])

# Get url list for pages
urls = [u]
for page in range(pLast + 1)[2:]:
  u1 = u + '?page=' + str(page)
  urls.append(u1)

# Save listings
id_list = []
for url in urls:
  r = urllib.urlopen(url).read()
  soup = BeautifulSoup(r, "lxml")
  listings = soup.find_all('li', class_ = 'listing')
  for tag in listings:
    id_list.append(tag['data-listingid'])

# Listing details
results = {}
i = 1
for id_num in id_list:
  print i
  i += 1
  u = 'https://www.rentler.com/listing/' + id_num
  r = urllib.urlopen(u).read()
  soup = BeautifulSoup(r, "lxml")

  price   = soup.find_all('h2'  , itemprop = 'price'          )[0].string
  address = soup.find_all('span', itemprop = 'streetAddress'  )[0].string
  city    = soup.find_all('span', itemprop = 'addressLocality')[0].string
  state   = soup.find_all('span', itemprop = 'addressRegion'  )[0].string
  zipcode = soup.find_all('span', itemprop = 'postalCode'     )[0].string
  lat     = soup.find_all('meta', itemprop = 'latitude' )[0].attrs['content']
  lon     = soup.find_all('meta', itemprop = 'longitude')[0].attrs['content']
  cat     = soup.find_all('meta', itemprop = 'category' )[0].attrs['content']
  stats   = soup.find_all('table', id = 'stats')[0]
  beds    = stats.find_all('div')[0].string
  baths   = stats.find_all('div')[1].string
  year    = stats.find_all('div')[2].string
  sqft    = stats.find_all('div')[3].string

  price   = locale.atoi(price.strip().strip('$'))
  cat     = cat.split(' > ')[1]

  results[id_num] = (price, address, city, state, zipcode,
                      lat, lon, cat, beds, baths, year, sqft)

# Results data frame
df = pd.DataFrame.from_dict(results, orient = 'index').reset_index()
df.rename(columns = {'index' : 'ID',
                     0  : 'Rent',
                     1  : 'Address',
                     2  : 'City',
                     3  : 'State',
                     4  : 'ZipCode',
                     5  : 'Latitude',
                     6  : 'Longitude',
                     7  : 'Category',
                     8  : 'Beds',
                     9  : 'Baths',
                     10 : 'Year',
                     11 : 'SqFt'},
          inplace = True)
