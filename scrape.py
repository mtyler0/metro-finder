import googlemaps
from datetime import datetime
from selenium.webdriver.common.by import By


def get_listings(driver):
    apt_links = driver.find_elements(By.XPATH, '//*[@id="placardContainer"]/ul/li/article/header/div/a[@class="property-link"]')

    listings = {}
    for a in apt_links:
        href = a.get_attribute('href')
        address = a.find_element(By.CLASS_NAME, 'property-address').text
        listings[href] = address

    return listings


def get_distances(listings: dict, api_key: str):
    gmaps = googlemaps.Client(key=api_key)
    now = datetime.now()
    destinations = [
        '2501 Huntington Ave, Alexandria, VA 22303',
        '2400 Eisenhower Ave, Alexandria, VA 22314',
        '1900 Ballenger Ave, Alexandria, VA 22314',
        '700 N. Braddock Rd, Alexandria, VA 22314',
        '3500 Potomac Ave, Alexandria, VA 22301',
        '450 National Ave, Arlington, VA 22202',
        '1750 S. Clark St, Arlington, VA 22202',
        '1250 S. Hayes St, Arlington, VA 22202',
        '2 S. Rotary Rd, Arlington, VA 22202',
        '600 Maryland Ave SW, Washington, DC 20024',
        '701 Pennsylvania Ave NW, Washington, DC 20004',
        '630 H St NW, Washington, DC 20001',
        '300 M St NW, Washington, DC 20001'
        ]

    stop_map = {}

        #     matrix = gmaps.distance_matrix(address, destinations, mode='driving', departure_time=now)
        #     duration = round(matrix['rows'][0]['elements'][0]['duration']['value'] / 60, 2)
        #     stop_map[address] = duration

    
    for address in listings.values():
        matrix = gmaps.distance_matrix(address, destinations, mode='driving', departure_time=now)
        destinations = matrix['destination_addresses']
        for j, row in enumerate(matrix['rows']):
            duration = round(row['elements'][0]['duration']['value'] / 60, 2)
            stop_map[destinations[j]] = duration
        
        
    return stop_map