import requests
import os

application_id = os.environ['TT_APP_ID']
api_key = os.environ['TT_API_KEY']


def record_departure_search_ids(departure_searches):
    search_ids = []
    for search in departure_searches:
        search_ids.append(search['id'])
    return search_ids


def filter_results(results, search_id):
    new_results = []
    for item in results:
        if item['search_id'] == search_id:
            new_results.append(item)
    return new_results


def get_pairs(coords):
    return [[item['lng'], item['lat']] for item in coords]


def get_overlap(departure_searches):
    """
    Takes in a list with any number of lat-long pairs (departure_searches),
    formats a call to the Travel Time multi-origin API,
    and returns the intersection of the travel regions.
    """

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
    results = response.json()['results']
    overlap = filter_results(results, 'overlap')

    return get_pairs(overlap[0]['shapes'][0]['shell'])
