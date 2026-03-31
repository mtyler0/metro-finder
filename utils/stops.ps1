curl "https://api.wmata.com/Rail.svc/json/jStationEntrances" -H "api_key: e29ebb494479455fb862d1feeec34cfc" -o stations_raw.json

python3 -c "
import json
with open('stations_raw.json') as f:
    data = json.load(f)
result = {}
for s in data['Stations']:
    name = s['Name']
    a = s['Address']
    addr = f\"{a['Street']}, {a['City']}, {a['State']} {a['Zip']}\"
    if name not in result:
        result[name] = addr
with open('dc_metro_stations.json', 'w') as out:
    json.dump({'dc_metro_stations': result}, out, indent=2)
print('Done!')
"