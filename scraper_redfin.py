
# Scrape sale listings on redfin.com
# using Beautiful Soup, requests

# Alec Myres
# July 2017

from bs4 import BeautifulSoup
import urllib, locale, requests, sys, time
import pandas as pd
import numpy as np

#sys.path.append('/usr/local/lib/python2.7/site-packages') 
#import selenium, time
#from selenium import webdriver

# Selenium/PhantomJS test
#driver = webdriver.PhantomJS(executable_path =
#         '/usr/local/bin/phantomjs-2.1.1-macosx/bin/phantomjs')
#driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
#time.sleep(3)
#print driver.find_element_by_id('content').text
#driver.close()

# ----------------------
# Scraping functions
# ----------------------

def getListingPagesCount(url):
  session = requests.Session()
  req = session.get(url, headers = headers)
  soup = BeautifulSoup(req.text, "lxml")
  t = soup.find('span', {'class':'pageText'}).text
  pLast = int(t.split(' ')[4])
  return pLast

def getListingPagesURLs(url, pLast):
  urls = [url]
  for page in range(pLast + 1)[2:]:
    u1 = url + '/page-' + str(page)
    urls.append(u1)
  return urls

def getListingIDs(urls):
  id_list = []
  for url in urls:
    time.sleep(np.random.uniform(.25, 1.0))
    session = requests.Session()
    req = session.get(url, headers = headers)
    soup = BeautifulSoup(req.text, "lxml")
    home_list = soup.find_all('a', {'class':'ViewDetailsButtonWrapper'})
    for h in home_list:
      id_list.append(h['href'])
  return id_list

def getListingDetails(id_value):
  time.sleep(np.random.uniform(0.25,1.0))
  url_id = 'https://www.redfin.com' + id_value
  session = requests.Session()
  req = session.get(url_id, headers = headers)
  soup = BeautifulSoup(req.text, "lxml")
  stats   = soup.find('div', {'class':'top-stats'})
  price   = stats.find('span', {'itemprop':'price'          })['content']
  address = stats.find('span', {'itemprop':'streetAddress'  })['title'  ]
  city    = stats.find('span', {'itemprop':'addressLocality'}).text.strip(', ')
  state   = stats.find('span', {'itemprop':'addressRegion'  }).text
  zipcode = stats.find('span', {'itemprop':'postalCode'     }).text
  lat     = stats.find('meta', {'itemprop':'latitude'       })['content']
  lon     = stats.find('meta', {'itemprop':'longitude'      })['content']
  price = int(price)
  lat   = float(lat)
  lon   = float(lon)
  facts = soup.find('div', {'class':'basic-info'})
  if facts == None:
    cat   = ''
    beds  = ''
    baths = ''
    year  = ''
    sqft  = ''
    lot   = ''
    reno  = ''
  else:
    rows = facts.find_all('div', {'class':'table-row'})
    ldict = {}
    for r in rows:
      ldict[r.find('span').string] = r.find('div' ).string
    cat   = ldict['Style']
    beds  = ldict['Beds' ]
    baths = ldict['Baths']
    year  = ldict['Year Built']
    sqft  = ldict['Finished Sq. Ft.'].replace(',','')
    lot   = ldict['Lot Size'].strip(' Sq. Ft.').replace(',','')
    reno  = ldict['Year Renovated']
  return (price, address, city, state, zipcode, lat, lon,
          cat, beds, baths, year, sqft, lot, reno)

# ----------------------
# Main Results
# ----------------------

zipcode = '84095'
url = 'https://www.redfin.com/zipcode/' + zipcode

# Add custom HTTP headers
ua1 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) '
ua2 = 'AppleWebKit/537.36 (KHTML, like Gecko) '
ua3 = 'Chrome/59.0.3071.115 Safari/537.36'
ac1 = 'text/html,application/xhtml+xml,application/xml;'
ac2 = 'q=0.9,image/webp,image/apng,*/*;q=0.8'
headers = {'User-Agent' : ua1 + ua2 + ua3,
           'Accept'     : ac1 + ac2}

pLast   = getListingPagesCount(url)
urls    = getListingPagesURLs(url, pLast)
id_list = getListingIDs(urls)

results = {}
for id_value in id_list:
  results[id_value] = getListingDetails(id_value)
  time.sleep(np.random.uniform(0.25,1.0))

df = pd.DataFrame.from_dict(results, orient = 'index').reset_index()
df.rename(columns = {'index' : 'ID',
                     0  : 'Price',
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
                     11 : 'SqFt',
                     12 : 'LotSize',
                     13 : 'YearReno'},
          inplace = True)

df.to_csv('redfin_' + zipcode + '.csv', encoding = 'utf-8')
