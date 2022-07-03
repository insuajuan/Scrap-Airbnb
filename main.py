import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.safari.options import Options


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


def get_rooms_url(page_url):
    rooms_list = list()
    href_list = get_all_href(page_url)
    for link in href_list:
        if '/rooms' in link:
            rooms_list.append(link)

    return rooms_list


def listing_pages(url, listings_per_page=20, pages_per_location=15):

    url_list = []
    for i in range(pages_per_location):
        offset = listings_per_page * i
        url_pagination = url + f'&items_offset={offset}'
        url_list.append(url_pagination)

    return url_list


def get_all_rooms_url(page_url):
    pages_to_scrap = listing_pages(page_url)
    rooms_list = list()
    for page in pages_to_scrap:
        rooms = get_rooms_url(page)
        rooms_list.append(rooms)

    return rooms_list


# prompt user for city, country, people, check-in, check-out
city = input('please provide city name. i.e: Buenos Aires\n')
city.replace(" ", "-")
country = input('please provide country name. i.e: Argentina\n')
country.replace(" ", "-")
adults = input('adults:\n')
checkin = input('checkin? YYYY-MM-DD\n')
checkout = input('checkout? YYYY-MM-DD\n')

homepage = 'http://www.airbnb.com'
main_listing = f'{homepage}/s/{city}--{country}/homes?adults={adults}&checkin={checkin}&checkout={checkout}'

# get links for all properties. Returns list of lists
# all_rooms_links = get_all_rooms_url(main_listing)
# iterate to open each link

example_property = 'https://www.airbnb.com.ar/rooms/41650674?adults=1&check_in=2022-10-10&check_out=2022-11-11&display_extensions%5B%5D=MONTHLY_STAYS&federated_search_id=265c03ad-7421-4d0c-8971-63e0b351da69&source_impression_id=p3_1656822314_80w88Md%2BQKxEEIdO'

# get price (need to use Selenium as there is JS that takes a second to load)
soup_property = scrape_page(example_property)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Safari(options=options)

driver.get(example_property)
time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
price = soup.find(class_="_1k4xcdh")
# response: $83.720 ARS
print(price.get_text())


property_name = soup.find('h1')
print(property_name.get_text())


driver.close()
