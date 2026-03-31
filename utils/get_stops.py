import json

with open('stations_raw.json') as f:
    data = json.load(f)

result = {}
for s in data['Stations']:
    name = s['Name']
    a = s['Address']
    addr = f"{a['Street']}, {a['City']}, {a['State']} {a['Zip']}"
    if name not in result:
        result[name] = {
            "address": addr,
            "lat": s['Lat'],
            "lon": s['Lon']
        }

with open('dc_metro_stations.json', 'w') as out:
    json.dump({'dc_metro_stations': result}, out, indent=2)

print(f"Done! {len(result)} stations written.")