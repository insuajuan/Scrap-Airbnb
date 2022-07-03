from bs4 import BeautifulSoup
import requests


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
    pages_to_scrap = listing_pages(properties_page)
    rooms_list = list()
    for page in pages_to_scrap:
        rooms = get_rooms_url(page)
        rooms_list.append(rooms)

    return rooms_list


homepage = 'http://www.airbnb.com'
properties_page = 'https://www.airbnb.com.ar/s/Buenos-Aires--Argentina/homes?adults=1&place_id=ChIJvQz5TjvKvJURh47oiC6Bs6A&checkin=2022-10-10&checkout=2022-11-11'


total_rooms_list = get_all_rooms_url(properties_page)

example_page = total_rooms_list[1]

