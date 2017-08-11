
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

def get_sale_pages_count(driver, zipcode, months):
    url = 'https://www.redfin.com'
    m = str(months)
    z = str(zipcode)
    search_url = url + '/zipcode/' + z + '/filter/include=sold-' + m + 'mo'
    driver.get(search_url)
    p = driver.find_element_by_class_name('pageText').text
    return p.split(' ')[4]

# --------------------
# MAIN
# --------------------

url = 'http://www.redfin.com'
chrome_path = '/Users/alecmyres/Applications/chromedriver'
email = '' # sys.argv[1]
password = '' # sys.argv[2]
driver = load_main_page(url, chrome_path)
driver = sign_in_redfin(driver, email, password)

# Search (zipcode, months)
search_url = 'https://www.redfin.com/zipcode/84095/filter/include=sold-6mo'

driver.close()
