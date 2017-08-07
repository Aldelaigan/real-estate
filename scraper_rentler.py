
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

def get_listing_page_count(url):
  r = urllib.urlopen(url).read()
  soup = BeautifulSoup(r, "lxml")
  p = soup.find('ul', {'class':'pager'})
  p = p.contents[1]
  pStr = p.a.string
  pFirst = int(pStr.split(' ')[1])
  pLast  = int(pStr.split(' ')[3])
  return p_last

def get_listing_pages_urls(url, p_last):
  urls = [url]
  for page in range(p_last + 1)[2:]:
    u1 = url + '?page=' + str(page)
    urls.append(u1)
  return urls

def get_listing_ids(urls):
  id_list = []
  for url in urls:
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    listings = soup.find_all('li', {'class':'listing'})
    for tag in listings:
      id_list.append(tag['data-listingid'])
  return id_list

def get_listing_details(id_num):
  u = 'https://www.rentler.com/listing/' + id_num
  r = urllib.urlopen(u).read()
  soup = BeautifulSoup(r, "lxml")
  price   = soup.find('h2'  , itemprop = 'price'          ).string
  address = soup.find('span', itemprop = 'streetAddress'  ).string
  city    = soup.find('span', itemprop = 'addressLocality').string
  state   = soup.find('span', itemprop = 'addressRegion'  ).string
  zipcode = soup.find('span', itemprop = 'postalCode'     ).string
  lat     = soup.find('meta', itemprop = 'latitude' ).attrs['content']
  lon     = soup.find('meta', itemprop = 'longitude').attrs['content']
  cat     = soup.find('meta', itemprop = 'category' ).attrs['content']
  stats   = soup.find('table', id = 'stats')
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

p_last  = get_listing_page_count(url)
urls    = get_listing_pages_urls(url, p_last)
id_list = get_listing_ids(urls)

results = {}
for id_num in id_list:
  results[id_num] = get_listing_details(id_num)
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
