import json, os
import scrape
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('API_KEY')

with open('data.txt') as f:
    listings = json.load(f)

res = scrape.get_distances(listings, api_key=api_key, mode='driving')
res = dict(sorted(res.items(), key=lambda item: item[1]['duration_mins']))
# print(res)

with open('out.txt', 'w') as f:
    json.dump(res, f, indent=4)