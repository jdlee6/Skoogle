from flask import redirect, url_for, render_template, request
import googlemaps, json, os, requests
from app.forms import SearchForm
from geopy.geocoders import Nominatim
from app import app, API_KEY, db
from app.models import Result


gmaps = googlemaps.Client(key=API_KEY)
query = ['skatepark', 'skate park']
default_url = 'https://maps.googleapis.com/maps/api/place/photo?'
width = '300'


def db_reset():
    db.drop_all()
    db.create_all()


@app.route('/')
@app.route('/home')
def home():
    form = SearchForm()
    return render_template('home.html', form=form)


@app.route('/results', methods=['GET', 'POST'])
def results():
    places_results = []
    form = SearchForm()

    geolocator = Nominatim(user_agent="myapplication")
    city = form.location.data
    location = geolocator.geocode(city)
    longitude = location.longitude
    latitude = location.latitude
    skatepark_result = gmaps.places(query=query[0] or query[1], radius=40000, location=f'{latitude}, {longitude}')

    for park in skatepark_result['results']:
        address = park['formatted_address']
        distance_response = gmaps.distance_matrix(origins=f'{latitude}, {longitude}', destinations=address, transit_mode='driving')
        distance = distance_response['rows'][0]['elements'][0]['distance']['text']
        duration = distance_response['rows'][0]['elements'][0]['duration']['text']

        # retrieve photo url (some don't have photos)
        try:
            for photo in park['photos']:
                reference = photo['photo_reference']
                photo_url = requests.get(default_url + 'maxwidth=' + width +'&photoreference=' + reference + '&key=' + API_KEY).url
        except Exception as e:
            print(f'{e}')

        entry = Result(origin=city,
                        name=park['name'],
                        address=park['formatted_address'],
                        rating=park['rating'],
                        distance=distance,
                        duration=duration,
                        photo=photo_url)
        places_results.append(entry)

        print(city, park['name'], address, park['rating'], distance, duration, photo_url)

    db_reset()
    db.session.add_all(places_results)
    db.session.commit()

    # pagination
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.paginate(page=page, per_page=5)

    return render_template('results.html', form=form, results=page_results)

''' Problem: When you click on the a page button it conducts
a brand new search but this time with no origin data which 
ultimately fails to load the next page . . . 
Works perfectly fine if I don't paginate it '''