
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

def get_listing_pages_count(url, headers):
  session = requests.Session()
  req = session.get(url, headers = headers)
  soup = BeautifulSoup(req.text, "lxml")
  t = soup.find('span', {'class':'pageText'}).text
  p_last = int(t.split(' ')[4])
  return p_last

def get_listing_pages_urls(url, p_last):
  urls = [url]
  for page in range(p_last + 1)[2:]:
    u1 = url + '/page-' + str(page)
    urls.append(u1)
  return urls

def get_listing_ids(urls, headers):
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

def get_listing_details(id_value, headers):
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
    sqft  = ''
    usqft = ''
    lot   = ''
    year  = ''
    reno  = ''
  else:
    rows = facts.find_all('div', {'class':'table-row'})
    ldict = {}
    for r in rows:
      t = r.find('div' ).string.replace(u'\u2014', '')
      ldict[r.find('span').string] = t
    cat   = ldict['Style'             ]
    beds  = ldict['Beds'              ]
    baths = ldict['Baths'             ]
    sqft  = ldict['Finished Sq. Ft.'  ].replace(',','')
    usqft = ldict['Unfinished Sq. Ft.'].replace(',','')
    lot   = ldict['Lot Size'          ]
    year  = ldict['Year Built'        ]
    reno  = ldict['Year Renovated'    ]
    lot   = acre_converter(lot)

  return (address, city, state, zipcode, lat, lon, cat,
          beds, baths, sqft, usqft, lot, year, reno, price)

def acre_converter(value):
  if 'Sq. Ft.' in value:
    v = value.strip(' Sq. Ft.').replace(',','')
    return round(float(v)/43560.0, 2)
  elif 'Acres' in value:
    v = value.strip(' Acres')
    return round(float(v),2)
  else:
    return value

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

p_last  = get_listing_pages_count(url, headers)
urls    = get_listing_pages_urls(url, p_last)
id_list = get_listing_ids(urls, headers)

results = {}
for id_value in id_list:
  results[id_value] = get_listing_details(id_value, headers)
  time.sleep(np.random.uniform(0.25,1.0))

df = pd.DataFrame.from_dict(results, orient = 'index').reset_index()
df.rename(columns = {'index' : 'ID',
                     0  : 'Address',
                     1  : 'City',
                     2  : 'State',
                     3  : 'ZipCode',
                     4  : 'Latitude',
                     5  : 'Longitude',
                     6  : 'Category',
                     7  : 'Beds',
                     8  : 'Baths',
                     9  : 'SqFt',
                     10 : 'UnSqFt',
                     11 : 'LotSize',
                     12 : 'YearBuilt'
                     13 : 'YearReno',
                     14 : 'Price'},
          inplace = True)

df.to_csv('redfin_' + zipcode + '.csv', encoding = 'utf-8')
