
# Alec Myres
# July 2017

from bs4 import BeautifulSoup
import requests, sys, time
import pandas as pd
import numpy as np

sys.path.append('/usr/local/lib/python2.7/site-packages')
import selenium
from selenium import webdriver
from selenium.webdriver.options import Options
from selenium.webdriver.support import expected_conditions as ec

# Selenium/PhantomJS test
#driver = webdriver.PhantomJS(executable_path =
#         '/usr/local/bin/phantomjs-2.1.1-macosx/bin/phantomjs')
#driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
#time.sleep(3)
#print driver.find_element_by_id('content').text
#driver.close()

#  Main page
url = 'http://www.redfin.com'
chrome_path = '/Users/alecmyres/Applications/chromedriver'
chrome_options = webdriver.Chrome.Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path = chrome_path,
                          chrome_options  = chrome_options)
driver.get(url)
time.sleep(2)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
driver.close()
 

ua1 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) '
ua2 = 'AppleWebKit/537.36 (KHTML, like Gecko) '
ua3 = 'Chrome/59.0.3071.115 Safari/537.36'
ac1 = 'text/html,application/xhtml+xml,application/xml;'
ac2 = 'q=0.9,image/webp,image/apng,*/*;q=0.8'
headers = {'User-Agent' : ua1 + ua2 + ua3,
           'Accept'     : ac1 + ac2}
session = requests.Session()
req = session.get(url, headers = headers)
soup = BeautifulSoup(req.text, 'lxml')

#  Click "Sign In"

#  Click "Continue with email"

#  Enter email, password, sign in


