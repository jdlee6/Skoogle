import googlemaps
from geopy.geocoders import Nominatim
from flask import current_app

gmaps = googlemaps.Client(key=current_app.config['API_KEY'])
geolocator = Nominatim(user_agent="myapplication")