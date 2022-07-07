import concurrent.futures
import time

from helpers import create_excel, get_all_rooms_url, get_property_info, store_to_excel
from tqdm import tqdm
from multiprocessing import Pool

# prompt user for city, country, people, check-in, check-out
# TO-DO: wrap around try except block. Validate user input
city = input('Please provide city name. i.e: Buenos Aires\n')
if city == "testing":
    city = 'Buenos Aires'
    country = "Argentina"
    checkin = "2022-10-20"
    checkout = "2022-11-20"
    adults = 1
    children = 0

else:
    city.replace(" ", "-")
    country = input('Please provide country name. i.e: Argentina\n')
    country.replace(" ", "-")
    adults = input('adults:\n') # min 1 max 16
    children = input('children:\n') # min 0 max 6
    checkin = input('checkin? YYYY-MM-DD\n')
    checkout = input('checkout? YYYY-MM-DD\n') # validate that is > checkin

print('**********************************')
print("Getting all urls to search for final prices")
print('**********************************')


# Main search URL
homepage = 'https://www.airbnb.com'
main_search = f'{homepage}/s/{city}--{country}/homes?' \
               f'adults={adults}&children={children}&checkin={checkin}&checkout={checkout}'


# get links for all properties. Returns list
all_rooms_links = get_all_rooms_url(main_search)
total_rooms = len(all_rooms_links)
print(f"Found {total_rooms} rooms in {city}. This may take about {round(total_rooms*0.85, 2)} seconds")

# iterate to open each link and save info to a dictionary
properties_dict = dict()

start = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(get_property_info, all_rooms_links)
    for result in results:
        property_name = result[0]
        price = result[1]
        url = result[2]
        properties_dict[property_name] = [price, url]

end = time.perf_counter()

print(f"Elapsed time: {end-start} seconds")
# for link in tqdm(all_rooms_links):
#     property_name, price = get_property_info(link)


# Create Excel Workbook
wb = create_excel(city, country, checkin, checkout, adults, children)
result_sheet = wb.active

# iterate over the property dictionary to write info to excel
store_to_excel(result_sheet, properties_dict)

# Save workbook and close driver
wb.save('Airbnb-results.xlsx')
