from gmaps_api import get_overlap


def unwrap_coords(response, coords_id):
    return response['results'][coords_id]['shapes'][0]['shell']


def get_pairs(coords):
    return [[str(item['lng']), str(item['lat'])] for item in coords]


def get_string(pairs):
    return '\n'.join([','.join(i) for i in pairs])


def filter_results(results, search_id):
    new_results = []
    for item in results:
        if item['search_id'] == search_id:
            new_results.append(item)
    return new_results


results = get_overlap().json()['results']
overlap = filter_results(results, 'A/B')

overlap_pairs = get_pairs(overlap[0]['shapes'][0]['shell'])
overlap_string = get_string(overlap_pairs)

print('overlap')
print(overlap_string)
