import sys, os, json, time, random

import googlemaps
import undetected_chromedriver as uc
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

import scrape

# Config
load_dotenv()
api_key = os.getenv('API_KEY')
debug = os.getenv('DEBUG')

# Get apartment link from user
link = input('Link: ')

# Initialize stealthy webdriver
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--proxy-server=http://user:pass@residential-proxy:port')

driver = uc.Chrome(options=options, headless=False, version_main=146)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        window.chrome = { runtime: {} };
    """
})


def human_delay(min_s=1.5, max_s=4.0):
    time.sleep(random.uniform(min_s, max_s))


def write_apts(listings: dict):
    with open('data.txt', 'w') as file:
        json.dump(listings, file, indent=2)


# Scrape
try:
    driver.get("https://www.google.com")
    human_delay(2, 4)

    driver.get(link)
    human_delay(3, 6)

    # Confirm
    title = driver.title
    print(f'>>Apartment {title[:21]}... located.\n>>Scraping in Progress')

    listings = scrape.get_listings(driver)
    res = scrape.get_distances(listings, api_key=api_key)
    res = dict(sorted(res.items(), key=lambda item: item[1]['duration_mins']))

    # Write results to output file
    with open('out.txt', 'w') as f:
        json.dump(res, f, indent=4)


except Exception as e:
    print(f'>> Scraping failed: {e}')
    
finally:
    try:
        driver.quit()
    except Exception:
        pass