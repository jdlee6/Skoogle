from flask import redirect, url_for, render_template
import googlemaps, json, os
from app.forms import SearchForm
from geopy.geocoders import Nominatim
from app import app, API_KEY, db
from app.models import Result


gmaps = googlemaps.Client(key=API_KEY)
query = ['skatepark', 'skate park']


@app.route('/')
@app.route('/home')
def home():
    form = SearchForm()
    return render_template('home.html', form=form)


@app.route('/results', methods=['GET', 'POST'])
def results():
    places_results = []
    form = SearchForm()
    db.create_all()
    geolocator = Nominatim(user_agent="myapplication")
    city = form.location.data
    location = geolocator.geocode(city)
    longitude = location.longitude
    latitude = location.latitude
    skatepark_result = gmaps.places(query=query[0] or query[1], radius=40000, location=f'{latitude}, {longitude}')

    for park in skatepark_result['results']:
        address = park['formatted_address']
        distance_response = gmaps.distance_matrix(origins=city, destinations=address, mode='driving')
        distance = distance_response['rows'][0]['elements'][0]['distance']['text']
        duration = distance_response['rows'][0]['elements'][0]['duration']['text']
        entry = Result(origin=city,
                        name=park['name'],
                        address=park['formatted_address'],
                        rating=park['rating'],
                        distance=distance,
                        duration=duration)
        places_results.append(entry)
        print(city, park['name'], address, park['rating'], distance, duration)

    db.session.add_all(places_results)
    db.session.commit()
    return render_template('results.html', form=form, results=places_results)