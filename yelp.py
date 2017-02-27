import json
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from urllib.parse import urljoin
from geo_tools import degrees_to_metres

BASE = "https://api.yelp.com/oauth2/"

def get_secrets():
    """ Load the yelp secrets file """
    with open("secrets.json") as f:
        secrets = json.load(f)
        return secrets['client_id'], secrets['client_secret']

def get_token(client_id, client_secret):
    """ Get a Yelp token using a client id/secret  """
    client = BackendApplicationClient(client_id=client_id)
    token_url = urljoin(BASE, 'token')
    oauth = OAuth2Session(client=client)
    return oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)

def get_serach_request(client_id, token, latitude, longitude, radius_degrees):
    """ Fire a search request at Yelp """
    yelp = OAuth2Session(client_id, token=token)
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'radius': int(max(degrees_to_metres(latitude, longitude, radius_degrees))),
        'limit': 500
    }
    return yelp.get('https://api.yelp.com/v3/businesses/search',params=params)

def search(client_id, token, latitude=37.786660, longitude=-122.396559, radius_degrees=0.005):
    """ Return business search data from Yelp """
    return json.loads(get_serach_request(client_id, token, latitude, longitude, radius_degrees).content.decode('utf-8'))

def main():
    client_id, client_secret = get_secrets()
    token = get_token(client_id, client_secret)
    print(search(client_id, token))

if __name__ == '__main__':
    main()