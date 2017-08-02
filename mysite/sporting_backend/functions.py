from rest_framework_jwt.settings import api_settings
import requests as r

def check_keys(key_list, keys):
    for needed_key in key_list:
        if needed_key not in keys:
            return needed_key
    return None


def who_is_my_law_maker(street_address, city, state):
    if not street_address or not city or not state:
        return None

    map_response = r.get(
        'https://maps.googleapis.com/maps/api/geocode/json?address='
        + street_address
        + ','
        + city
        + ',' + state
    )
    map_response_json = map_response.json()
    if len(map_response_json['results']) != 1:
        return None
    lat = str(map_response_json['results'][0]['geometry']['location']['lat'])
    lng = str(map_response_json['results'][0]['geometry']['location']['lng'])

    sunlight_response = r.get(
        'http://congress.api.sunlightfoundation.com/legislators/locate'
        + '?latitude=' + lat
        + '&longitude=' + lng
    )
    sunlight_results = sunlight_response.json()['results']
    return sunlight_results