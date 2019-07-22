import googlemaps
from flask import current_app

gmaps = googlemaps.Client(key=current_app.config['API_KEY'])