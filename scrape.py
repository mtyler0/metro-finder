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


def get_distances(listings: dict):
    pass
