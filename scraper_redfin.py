
# Scrape sale listings on redfin.com
# using Beautiful Soup, requests

# Alec Myres
# July 2017

from bs4 import BeautifulSoup
import urllib, locale, requests, sys, time
import pandas as pd
import numpy as np


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
    cat   = ldict['Style'] if 'Style' in ldict else ''
    beds  = ldict['Beds' ] if 'Beds'  in ldict else ''
    baths = ldict['Baths'] if 'Baths' in ldict else ''
    sqft  = ldict['Finished Sq. Ft.'  ] if 'Finished Sq. Ft.'   in ldict else ''
    usqft = ldict['Unfinished Sq. Ft.'] if 'Unfinished Sq. Ft.' in ldict else ''
    lot   = ldict['Lot Size'      ] if 'Lot Size'       in ldict else ''
    year  = ldict['Year Built'    ] if 'Year Built'     in ldict else ''
    reno  = ldict['Year Renovated'] if 'Year Renovated' in ldict else ''
    sqft  = sqft.replace(',','')
    usqft = usqft.replace(',','')
    lot   = acre_converter(lot)
  return (price, address, city, state, zipcode, lat, lon,
          cat, beds, baths, sqft, usqft, lot, year, reno)

def acre_converter(value):
  if 'Sq. Ft.' in value:
    v = value.strip(' Sq. Ft.').replace(',','')
    return round(float(v)/43560.0, 2)
  elif 'Acres' in value:
    v = value.strip(' Acres')
    return round(float(v),2)
  elif ',' in value:
    v = value.replace(',','')
    return round(float(v)/43560.0, 2)
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
                     10 : 'SqFt',
                     11 : 'UnSqFt',
                     12 : 'LotSize',
                     13 : 'YearBuilt',
                     14 : 'YearReno'},
          inplace = True)

df.to_csv('redfin_' + zipcode + '.csv', encoding = 'utf-8')
