from helpers import create_excel, get_all_rooms_url, get_property_info, store_to_excel
from tqdm import tqdm

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


# Create Excel Workbook
wb = create_excel(city, country, checkin, checkout, adults, children)
result_sheet = wb.active

# Main search URL
homepage = 'http://www.airbnb.com'
main_listing = f'{homepage}/s/{city}--{country}/homes?' \
               f'adults={adults}&children={children}&checkin={checkin}&checkout={checkout}'


# get links for all properties. Returns list of lists
print('**********************************')
print("Getting all urls to search for final prices")

all_rooms_links = get_all_rooms_url(main_listing)

# iterate to open each link and save info to a dictionary
properties_dict = dict()
for link in tqdm(all_rooms_links):
    property_name, price = get_property_info(homepage+link)
    properties_dict[property_name] = [price, homepage+link]
#
# # iterate over the property dictionary to write info to excel
store_to_excel(result_sheet, properties_dict)
#
# # Save workbook and close driver
wb.save('Airbnb-results.xlsx')
