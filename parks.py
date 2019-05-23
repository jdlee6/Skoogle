#!/usr/local/bin/python3.7
# parks.py - this python script will be used to locate skateparks within a 25 mile radius

import googlemaps, pprint, time, json, sys
from geopy.geocoders import Nominatim

# Finding user location based on input() 
geolocator = Nominatim(user_agent="myapplication")
try:
    city = input('Please enter the city or zip code you want to search for: ')
    location = geolocator.geocode(city)
    longitude = location.longitude
    latitude = location.latitude
except Exception as e:
    print(f'Error:{city} does not exist!')
    sys.exit()

with open('config.json') as config:
    config_data = json.load(config)

# Define API key from json file
API_KEY = config_data['Keys']['GoogleAPIKey']

# Define our Client
gmaps = googlemaps.Client(key=API_KEY)

query = ['skatepark', 'skate park']
skatepark_result = gmaps.places(query=query[0] or query[1], radius=40000, location=f'{latitude}, {longitude}')

for park in skatepark_result['results']:
    # define place_id
    my_place_id = park['place_id']
    # define fields that we want returned to us
    my_fields = ['name', 'rating']
    # set parameters
    park_details = gmaps.place(place_id=my_place_id, fields=my_fields)

    pprint.pprint(park_details['result'])



# pprint.pprint(skatepark_result)
# print(park['place_id'], park['name'])
