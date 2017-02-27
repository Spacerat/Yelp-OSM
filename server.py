import gevent
from gevent import monkey
monkey.patch_all()
from gevent.wsgi import WSGIServer
from flask import Flask, jsonify, request
from flask_caching import Cache
import logging
from gzipped import gzipped
import openstreetmap
import yelp 


app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=10000)
def get_yelp_data():
    """ Make sure we cache the token, so we only have to fetch it once every so often.
    We could actually do something more interesting and set timeout=token-expiry, but it's not worth it here.
    """
    client_id, client_secret = yelp.get_secrets()
    token = yelp.get_token(client_id, client_secret)
    return client_id, token

def search_yelp(client_id, token, latitude, longitude, size):
    return ('yelp', yelp.search(client_id, token))

def search_osm(latitude, longitude, size):
    return ('osm', openstreetmap.search(latitude, longitude, size))

@cache.memoize(timeout=30)
def search_both(latitude, longitude, size):
    """ Fetch data form OSM and Yelp in parallel """
    client_id, token = get_yelp_data()
    args = (latitude, longitude, size)
    results = gevent.joinall([
        gevent.spawn(search_osm, *args),
        gevent.spawn(search_yelp, client_id, token, *args)
    ])

    return dict(v.value for v in results)

@app.route('/search')
@gzipped
def search():
    """ Endpoint for /search.
    Example request: http://localhost:5000/search?size=0.001&lat=37.786660&lon=-122.396559
    """
    latitude = float(request.args['lat'])
    longitude = float(request.args['lon'])
    size = float(request.args['size'])
    result = search_both(latitude, longitude, size)
    return jsonify(result)

http_server = WSGIServer(('', 5000), app)