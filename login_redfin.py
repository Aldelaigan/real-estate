
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

# Selenium/PhantomJS test
#driver = webdriver.PhantomJS(executable_path =
#         '/usr/local/bin/phantomjs-2.1.1-macosx/bin/phantomjs')
#driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
#time.sleep(3)
#print driver.find_element_by_id('content').text
#driver.close()

#  Load main page
url = 'http://www.redfin.com'
chrome_path = '/Users/alecmyres/Applications/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path = chrome_path,
                          chrome_options  = chrome_options)
driver.get(url)
time.sleep(1)
#page_source = driver.page_source
#soup = BeautifulSoup(page_source, 'lxml')

#  Click "Sign In"
try:
    element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.LINK_TEXT, 'Sign In')))
finally:
    signin_link = driver.find_element_by_link_text('Sign In')
    signin_link.click()

#  Click "Continue with email"
try:
    element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'emailSignInButton')))
finally:
    signin_email = driver.find_element_by_class_name('emailSignInButton')
    signin_email.click()

# Enter email, password, sign in
try:
    element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'input')))
finally:
    email = ''
    passw = ''

    # ISSUES HERE...
    # "ElementNotVisibleException"
    input1 = driver.find_element_by_name('emailInput')
    input1.send_keys(email)

    submit_button = driver.find_element_by_class_name('submitButton')
    submit_button.click()

# Perform search

# Get results

driver.close()
