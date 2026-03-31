import json
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


def chunked(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def get_distances(listings: dict, mode: str='walking', api_key: str=None):
    gmaps = googlemaps.Client(key=api_key)
    now = datetime.now()
    
    with open('data\\dc_metro_stations.json') as f:
        stations = json.load(f)['dc_metro_stations']

    destinations = [(s['lat'], s['lon']) for s in stations.values()]
    names = list(stations.keys())

    results = {}


    for link, address in listings.items():
        all_elements = []

        for dest_chunk, name_chunk in zip(chunked(destinations, 25), chunked(names, 25)):
            try:
                matrix = gmaps.distance_matrix(address, dest_chunk, mode=mode)
            except Exception as e:
                raise RuntimeError(f'Distance matrix request failed: {e}')
        all_elements.extend(zip(name_chunk, matrix['rows'][0]['elements']))

        stop_map = {stop: element['duration']['value'] 
                    for stop, element in all_elements
                    if element['status'] == 'OK'}

        if not stop_map:
            results[address] = {'closest_stop': None, 'duration_mins': None}
            continue
        
        closest= min(stop_map, key=stop_map.get)

        station_data = stations[closest]
        directions_link = (
            f"https://www.google.com/maps/dir/?api=1"
            f"&origin={address.replace(' ', '+')}"
            f"&destination={station_data['lat']},{station_data['lon']}"
            f"&travelmode={mode}"
        )
        
        results[address] = {
            'link': link,
            'closest_station': closest,
            'duration_mins': round(stop_map[closest] / 60, 2),
            'directions_link': directions_link
                            }
        
    return results