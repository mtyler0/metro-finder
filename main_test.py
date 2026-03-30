import json, os
import scrape
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('API_KEY')

with open('data.txt') as f:
    listings = json.load(f)

#top_5_closest = sorted(list(.values()))[:5]

stop_map = scrape.get_distances(listings, api_key)
print(stop_map)