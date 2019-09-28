import requests
import os

application_id = os.environ['TT_APP_ID']
api_key = os.environ['TT_API_KEY']


def get_overlap():
    response = requests.post(
        'http://api.traveltimeapp.com/v4/time-map',
        headers={
            'Content-Type': 'application/json',
            'X-Application-Id': application_id,
            'X-Api-Key': api_key
        },
        json={
            "departure_searches": [
                {
                    "id": "A",
                    "coords": {
                        "lat": 51.507609,
                        "lng": -0.128315
                    },
                    "transportation": {
                        "type": "public_transport"
                    },
                    "departure_time": "2019-09-27T08:00:00Z",
                    "travel_time": 900
                },
                {
                    "id": "B",
                    "coords": {
                        "lat": 51.510918,
                        "lng": -0.117268
                    },
                    "transportation": {
                        "type": "walking"
                    },
                    "departure_time": "2019-09-27T08:00:00Z",
                    "travel_time": 600
                }
            ],
            "intersections": [
                {
                    "id": "A/B",
                    "search_ids": ["A", "B"]
                }
            ]
        }
    )

    return response
