import os
from dotenv import load_dotenv

from google.maps import places_v1
from google.type import latlng_pb2
from google.geo.type import Viewport

load_dotenv()
api_key = os.getenv('API_KEY')

client = places_v1.PlacesClient(
    client_options={"api_key": api_key}
)

viewport = places_v1.SearchTextRequest.LocationRestriction(
    rectangle=Viewport(
        low=latlng_pb2.LatLng(latitude=38.766506, longitude=-77.340055),
        high=latlng_pb2.LatLng(latitude=39.119912, longitude=-76.842033)
    )
)

request = places_v1.SearchTextRequest(
    text_query='metro center',
    location_restriction=viewport
)

response = client.search_text(
    request=request,
    metadata=[("x-goog-fieldmask", "places.id,places.displayName")]
)


for place in response.places:
    print(place.display_name.text, place.formatted_address)