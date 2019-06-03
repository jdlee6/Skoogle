from flask import redirect, url_for, render_template
import googlemaps, json, os
from app.forms import SearchForm
from geopy.geocoders import Nominatim
from app import app, API_KEY


gmaps = googlemaps.Client(key=API_KEY)
query = ['skatepark', 'skate park']


@app.route('/')
@app.route('/home')
def home():
    form = SearchForm()
    return render_template('home.html', form=form)


@app.route('/results', methods=['GET', 'POST'])
def results():
    form = SearchForm()
    geolocator = Nominatim(user_agent="myapplication")
    city = form.location.data
    location = geolocator.geocode(city)
    longitude = location.longitude
    latitude = location.latitude

    # json data of skatepark_result based on our location from the search bar
    skatepark_result = gmaps.places(query=query[0] or query[1], radius=40000, location=f'{latitude}, {longitude}')
    places_response = json.dumps(skatepark_result['results'])
    load_r = json.loads(places_response)

    # get address variable for now  
    load_d = dict()
    list_of_distances = list()
    list_of_durations = list()

    for park in skatepark_result['results']:
        address = park['formatted_address']
        distance_response = gmaps.distance_matrix(origins=city, destinations=address, mode='driving')
        list_of_distances.append(distance_response['rows'][0]['elements'][0]['distance']['text'])
        list_of_durations.append(distance_response['rows'][0]['elements'][0]['duration']['text'])

    load_d = list(zip(list_of_distances, list_of_durations))
    index = 0
    for parks in load_r:
        parks['distance'] = load_d[index][0]
        parks['duration'] = load_d[index][1]
        index += 1

    # right here, load_d has last reference from the for loop ^^^
    return render_template('results.html', form=form, response=load_r)