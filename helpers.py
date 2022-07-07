import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import openpyxl

from tqdm import tqdm


def scrape_page(page_url):

    resp = requests.get(page_url)
    content = resp.content
    soup = BeautifulSoup(content, features='html.parser')

    return soup


def get_all_href(page_url):
    href_list = list()
    html_content = scrape_page(page_url)
    for link in html_content.find_all('a'):
        href = link.get('href')
        href_list.append(href)
    return href_list


def listing_pages(url, listings_per_page=20, pages_per_location=15):

    url_list = []
    for i in range(pages_per_location):
        offset = listings_per_page * i
        url_pagination = url + f'&items_offset={offset}'
        url_list.append(url_pagination)

    return url_list


def get_all_rooms_url(page_url):
    url_pages_list = listing_pages(page_url)

    rooms_list = list()
    for page in tqdm(url_pages_list):
        href_list = get_all_href(page)
        for i in range(len(href_list) - 1):
            if '/rooms' in href_list[i] and href_list[i - 1] != href_list[i]:
                rooms_list.append("https://www.airbnb.com"+href_list[i])

    return rooms_list


def get_property_info(url):
    # Create Selenium driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    # get price (need to use Selenium as there is JS that takes a second to load)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_1k4xcdh")))

    # after waiting, get price and property name
    price = driver.find_element(By.CLASS_NAME, "_1k4xcdh").text
    property_name = driver.find_element(By.TAG_NAME, "h1").text

    print(f"Got info for property {property_name}")

    driver.close()

    return property_name, price, url


def create_excel(city, country, checkin, checkout, adults, children):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Results"

    b2 = sheet['B2']
    b2.value = "Location"
    c2 = sheet['C2']
    c2.value = f"{city} - {country}"

    b3 = sheet['B3']
    b3.value = "Check In"
    c3 = sheet['C3']
    c3.value = checkin

    b4 = sheet['B4']
    b4.value = "Check Out"
    c4 = sheet['C4']
    c4.value = checkout

    b5 = sheet['B5']
    b5.value = "Adults"
    c5 = sheet['C5']
    c5.value = adults

    b6 = sheet['B6']
    b6.value = "Children"
    c6 = sheet['C6']
    c6.value = children

    b8 = sheet['B8']
    b8.value = "Property"
    c8 = sheet['C8']
    c8.value = "Price"
    d8 = sheet['D8']
    d8.value = "Link"

    return workbook


def store_to_excel(sheet, prop_dict):
    # i=9 because we start writing excel data in cell row 9
    i = 9
    for key in prop_dict:
        # B column is for property name
        sheet[f"B{i}"].value = key
        # C column is for price
        price = prop_dict[key][0]
        sheet[f"C{i}"].value = price
        # D column is for link
        link = prop_dict[key][1]
        sheet[f"D{i}"].value = link

        i += 1