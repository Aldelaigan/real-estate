
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

def get_sale_search_url(zipcode, months):
    # months = {3,6,12,24}
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
p_last = get_sale_pages_count(driver, search_url)
urls   = get_sale_pages_urls(search_url, p_last)
id_list = get_sale_ids(driver, urls) 


driver.get(search_url)


driver.close()
