import googlemaps
from flask import current_app
from geopy.geocoders import Nominatim


gmaps = googlemaps.Client(key=current_app.config['API_KEY'])
geolocator = Nominatim(user_agent="myapplication")