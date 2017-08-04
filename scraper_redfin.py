
from bs4 import BeautifulSoup
import urllib, locale, requests, sys, time
#sys.path.append('/usr/local/lib/python2.7/site-packages')
import pandas as pd
import numpy as np
#import selenium, time
#from selenium import webdriver

# Selenium/PhantomJS test
#driver = webdriver.PhantomJS(executable_path =
#         '/usr/local/bin/phantomjs-2.1.1-macosx/bin/phantomjs')
#driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
#time.sleep(3)
#print driver.find_element_by_id('content').text
#driver.close()

# Add custom HTTP headers
zipcode = '84095'
url = 'https://www.redfin.com/zipcode/' + zipcode
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari\
/537.36',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}


def getListingsPagesCount(url):
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
  i = 1
  id_list = []
  for url in urls:
    time.sleep(np.random.uniform(.25, 1.0))
    req = session.get(url, headers = headers)
    soup = BeautifulSoup(req.text, "lxml")
    home_list = soup.find_all('a', {'class':'ViewDetailsButtonWrapper'})
    for h in home_list:
      print i
      i += 1
      id_list.append(h['href'])
  return id_list

def getListingDetails(id_value):
  time.sleep(np.random.uniform(0.25,1.0))
  url = 'https://www.redfin.com' + id_value
  session = requests.Session()
  req = session.get(url, headers = headers)
  soup = BeautifulSoup(req.text, "lxml")
  stats   = soup.find('div', {'class':'top-stats'})
  price   = stats.find('span', {'itemprop':'price'          })['content']
  address = stats.find('span', {'itemprop':'streetAddress'  })['title'  ]
  city    = stats.find('span', {'itemprop':'addressLocality'}).text.strip(', ')
  state   = stats.find('span', {'itemprop':'addressRegion'  }).text
  zipcode = stats.find('span', {'itemprop':'postalCode'     }).text
  lat     = stats.find('meta', {'itemprop':'latitude'       })['content']
  lon     = stats.find('meta', {'itemprop':'longitude'      })['content']
  category
  beds
  baths
  year
  sqft

soup.find('div', {'class':'basic-info'})


pLast = getListingsPagesCount(url)
urls  = getListingPagesURLs(url, pLast)
id_list = getListingIDs(urls)
