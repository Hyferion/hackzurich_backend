import requests
import os

application_id = os.environ['TT_APP_ID']
api_key = os.environ['TT_API_KEY']


def record_departure_search_ids(departure_searches):
    search_ids = []
    for search in departure_searches:
        search_ids.append(search['id'])
    return search_ids


"""
Takes in a list with any number of lat-long pairs (departure_searches),
formats a call to the Travel Time multi-origin API,
and returns the intersection of the travel regions.
"""


def get_overlap(departure_searches):
    departure_search_ids = record_departure_search_ids(departure_searches)

    response = requests.post(
        'http://api.traveltimeapp.com/v4/time-map',
        headers={
            'Content-Type': 'application/json',
            'X-Application-Id': application_id,
            'X-Api-Key': api_key
        },
        json={
            "departure_searches": departure_searches,
            "intersections": [
                {
                    "id": "overlap",
                    "search_ids": departure_search_ids
                }
            ]
        }
    )

    return response
