import requests
import os

api_key = os.environ['GMAPS_API_KEY']


def get_nearby_places(centroid, radius, type):
    response = requests.get(
        'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
        params={
            'key': api_key,
            'location': ','.join(map(str, centroid)),
            'radius': radius,
            'type': type
        }
    )

    return response
