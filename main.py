import concurrent.futures
from helpers import create_excel, get_all_rooms_url, get_property_info, store_to_excel, user_input

# prompt user for city, country, people, check-in, check-out
city, country, adults, children, checkin, checkout = user_input()

print('**********************************')
print("Getting all urls to search for final prices")
print('**********************************')


# Main search URL
homepage = 'https://www.airbnb.com'
main_search = f'{homepage}/s/{city}--{country}/homes?' \
               f'adults={adults}&children={children}&checkin={checkin}&checkout={checkout}'

try:
    # get links for all properties. Returns list
    all_rooms_links = get_all_rooms_url(main_search)
    total_rooms = len(all_rooms_links)
    print(f"Found {total_rooms} rooms in {city}. This may take about {round(total_rooms*0.85, 2)} seconds")

    # iterate to open each link and save info to a dictionary
    properties_dict = dict()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(get_property_info, all_rooms_links)
        for result in results:
            property_name = result[0]
            price = result[1]
            url = result[2]
            properties_dict[property_name] = [price, url]

    # Create Excel Workbook
    wb = create_excel(city, country, checkin, checkout, adults, children)
    result_sheet = wb.active

    # iterate over the property dictionary to write info to excel
    store_to_excel(result_sheet, properties_dict)

    # Save workbook and close driver
    wb.save('Airbnb-results.xlsx')

except Exception as e:
    print(f"Error while accessing the URL. Please review your input and try again.\nError: {e}")
