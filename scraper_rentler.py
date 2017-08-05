
# Scrape rental listings on rentler.com
# using Beautiful Soup

# Alec Myres
# July 2017

from bs4 import BeautifulSoup
import urllib, locale, time
import pandas as pd
import numpy as np
locale.setlocale(locale.LC_ALL, 'en_US.UTF8') # price conversions

# ----------------------
# Scraping functions
# ----------------------

def getListingPageCount(url):
  r = urllib.urlopen(url).read()
  soup = BeautifulSoup(r, "lxml")
  p = soup.find_all('ul', class_ = 'pager')[0]
  p = p.contents[1]
  pStr = p.a.string
  pFirst = int(pStr.split(' ')[1])
  pLast  = int(pStr.split(' ')[3])
  return pLast

def getListingPagesURLs(url, pLast):
  urls = [url]
  for page in range(pLast + 1)[2:]:
    u1 = url + '?page=' + str(page)
    urls.append(u1)
  return urls

def getListingIDs(urls):
  id_list = []
  for url in urls:
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    listings = soup.find_all('li', class_ = 'listing')
    for tag in listings:
      id_list.append(tag['data-listingid'])
  return id_list

def getListingDetails(id_num):
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
  return (price, address, city, state, zipcode, lat, lon, cat, beds, baths, year, sqft)  


# ----------------------
# Main Results
# ----------------------

state = 'ut'
city  = 'south-jordan'
url = 'https://www.rentler.com/listings/' + state + '/' + city

pLast   = getListingPageCount(url)
urls    = getListingPagesURLs(url, pLast)
id_list = getListingIDs(urls)

results = {}
for id_num in id_list:
  results[id_num] = getListingDetails(id_num)
  time.sleep(np.random.uniform(0.25,1.0))
  
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
