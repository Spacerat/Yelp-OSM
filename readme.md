# Yelp + OpenStreetMap

A toy app which fetches both Yelp and OpenStreetMap data from the same location, in one request.

## Installation

Keep in mind that this was written in and only tested for Python 3. First, install the dependencies

    pip install -r requiremenets.txt

Then set up a secrets.json file for Yelp

``` json
{
    "client_id": "<your yelp client id>",
    "client_secret": "<your yelp client secret>"
}
```

Then run the server

    export FLASK_APP=server.py
    flask run

## Testing

Try navigating to http://localhost:5000/search?size=0.0001&lat=37.786660&lon=-122.396559

The length of time taken to process the request gets becomes fairly huge as size is increased; this is mostly due to OpenStreetMap's XML files being so massive.

## Notes on the code

- Gevent is used to execute the HTTP requests in parallel
- The Yelp API requires metres, OpenStreetMap uses degrees. `geo_tools.py` is used to convert degrees to metres for Yelp.


