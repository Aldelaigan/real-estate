
# Log into Redfin

# Alec Myres
# August 2017

from bs4 import BeautifulSoup
import requests, sys, time
import pandas as pd
import numpy as np
sys.path.append('/usr/local/lib/python2.7/site-packages')
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# ----------------------
# Functions
# ----------------------

def load_main_page(url, crome_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path = chrome_path,
                              chrome_options  = chrome_options)
    driver.get(url)
    try:
        element = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'OneLineHeader')))
    finally:
        return driver

def sign_in_redfin(driver, email, password):
    try:
        element = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.LINK_TEXT, 'Sign In')))
    finally:
        signin_link = driver.find_element_by_link_text('Sign In')
        signin_link.click()
    try:
        element = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'emailSignInButton')))
    finally:
        signin_email = driver.find_element_by_class_name('emailSignInButton')
        signin_email.click()
    try:
        driver.maximize_window()
        element = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'input')))
    finally:
        input1 = driver.find_element_by_xpath("//input[@placeholder='Email']")
        input2 = driver.find_element_by_xpath("//input[@placeholder='Password']")
        input1.send_keys(email)
        input2.send_keys(password)
        submit = driver.find_element_by_class_name('submitButton')
        submit.click()
        return driver

# Get url for search results, months in {3,6,12,24}
def get_sale_search_url(zipcode, months):
    url = 'https://www.redfin.com'
    z = str(zipcode)
    if months in [12,24]:
        y = int(months) / 12
        y = str(y)
        search_url = url + '/zipcode/' + z + '/filter/include=sold-' + y + 'yr'
        return search_url
    elif months in [3,6]:
        m = str(months)
        search_url = url + '/zipcode/' + z + '/filter/include=sold-' + m + 'mo'
        return search_url
    else:
        return 'Error with months'

def get_sale_pages_count(driver, search_url):
    try:
        driver.get(search_url)
        p = driver.find_element_by_class_name('pageText').text
        return int(p.split(' ')[4])
    except:
        return 'Error finding pages count'

def get_sale_pages_urls(search_url, p_last):
    urls = [search_url]
    for page in range(p_last + 1)[2:]:
        u1 = search_url + '/page-' + str(page)
        urls.append(u1)
    return urls

# Get list of ids (individual urls)
def get_sale_ids(driver, urls):
    id_list = []
    for url in urls:
        print url
        try:
            driver.get(url)
            element = WebDriverWait(driver, 15).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'link')))
        finally:
            time.sleep(np.random.uniform(0.5, 1.0))
            driver.maximize_window()
            links = driver.find_elements_by_xpath("//a[@class='link']") 
            for link in links:
                sale_path = link.get_property('href')
                if sale_path not in id_list:
                    id_list.append(sale_path)
    return id_list

def get_sale_details(driver, id_value):
    time.sleep(np.random.uniform(0.25,1.0))
    driver.get(id_value)
    # Location info
    ts  = "//div[@class='top-stats']"
    adr = "//span[@itemprop='streetAddress']"
    cty = "//span[@itemprop='addressLocality']"
    stt = "//span[@itemprop='addressRegion']"
    zpc = "//span[@itemprop='postalCode']"
    lat = "//meta[@itemprop='latitude']"
    lon = "//meta[@itemprop='longitude']"
    address   = driver.find_element_by_xpath(ts + adr).text
    city      = driver.find_element_by_xpath(ts + cty).text
    city      = city.strip(',')
    state     = driver.find_element_by_xpath(ts + stt).text
    zipcode   = driver.find_element_by_xpath(ts + zpc).text
    latitude  = driver.find_element_by_xpath(ts + lat)
    longitude = driver.find_element_by_xpath(ts + lon)
    latitude  =  latitude.get_property('content')
    longitude = longitude.get_property('content')
    # House characteristics
    ftb = "//div[@class='facts-table']//*[@class='table-row']"
    fdict = {}
    fact_rows = driver.find_elements_by_xpath(ftb)
    for row in fact_rows:
        key = row.find_element_by_class_name('table-label').text
        value = row.find_element_by_class_name('table-value').text
        fdict[key] = value
    baths = fdict['Baths']
    beds  = fdict['Beds']
    floor = fdict['Floors']
    style = fdict['Style']
    sqftf = fdict['Finished Sq. Ft.'].replace(',','')
    sqftu = fdict['Unfinished Sq. Ft.'].replace(',','')
    sqftt = fdict['Total Sq. Ft.'].replace(',','')
    lotsz = fdict['Lot Size']
    yearb = fdict['Year Built']
    yearr = fdict['Year Renovated']
    apn   = fdict['APN']
    # Tax assessment values
    txb = "//div[@class='tax-table']//tr"
    tax_rows = driver.find_elements_by_xpath(txb)
    tdict = {}
    for row in tax_rows:
        key = row.find_element_by_class_name('heading').text
        val = row.find_element_by_class_name('value'  ).text
        tdict[key] = val
    lnd_val = tdict['Land'     ].strip('$').replace(',','')
    add_val = tdict['Additions'].strip('$').replace(',','')
    tot_val = tdict['Total'    ].strip('$').replace(',','')
    # Sale Info
    #spx = "//div[@data-rf-test-id='abp-price']"
    #svl = "//div[@class='statsValue']"
    #sdt = "//span[@class='statsLabel']"
    #price   = driver.find_element_by_xpath(ts + spx + svl).text
    #sale_dt = driver.find_element_by_xpath(ts + spx + sdt).text

#SALE TYPE
#LOCATION
#DAYS ON MARKET
#HOA

# --------------------
# MAIN
# --------------------

url = 'http://www.redfin.com'
zipcode = 84095
months = 12
chrome_path = '/Users/alecmyres/Applications/chromedriver'
creds = pd.read_csv('credentials.csv', index_col = 'SITE')
email = creds['USERNAME']['Redfin']
pword = creds['PASSWORD']['Redfin']
driver = load_main_page(url, chrome_path)
driver = sign_in_redfin(driver, email, pword)


s_url  = get_sale_search_url(zipcode, months)
p_last = get_sale_pages_count(driver, s_url)
urls   = get_sale_pages_urls(s_url, p_last)
id_list = get_sale_ids(driver, urls) 




ziplist = [84095, # South Jordan
           84096, # Herriman
           84065, # Riverton/Bluffdale
           84088, # West Jordan (S)
           84084, # West Jordan (N)
           84081, # West Jordan (W)
           84043, # Lehi
           84003, # American Fork
           84005, # Eagle Mountain
           84045] # Saratoga Springs



#driver.get(search_url)
#driver.close()
