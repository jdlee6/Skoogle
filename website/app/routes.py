from flask import redirect, url_for, render_template, request
import googlemaps, json, os, requests
from app.forms import SearchForm
from geopy.geocoders import Nominatim
from app import app, API_KEY, db
from app.models import Result
from app.classes.Park import Park
import time

gmaps = googlemaps.Client(key=API_KEY)
query = ['skatepark', 'skate park']
default_url = 'https://maps.googleapis.com/maps/api/place/photo?'
width = '300'


def db_reset():
    db.drop_all()
    db.create_all()


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    return render_template('home.html', form=form)


def build_destination(name, destinations, distances, durations):
    # [(destination, distance, duration)]
    return list(zip(name, destinations, distances, durations))


def make_parks(data):
    return (Park(x) for x in data)


def miles_to_meters(miles):
    return int(float(miles)*1609.344)


@app.route('/results', methods=['GET', 'POST'])
def results():
    start = time.time()
    places_results = []
    form = SearchForm()
    DISTANCE_RADIUS = miles_to_meters(form.radius.data)
    # DISTANCE_RADIUS = 400000
    if form.validate_on_submit():
        geolocator = Nominatim(user_agent="myapplication")
        global city
        city = form.location.data
        location = geolocator.geocode(city)
        longitude = location.longitude
        latitude = location.latitude
        skatepark_result = gmaps.places(
            query=query[0] or query[1],
            radius=DISTANCE_RADIUS,
            location=f'{latitude}, {longitude}')['results']
        address_list = [park['formatted_address'] for park in skatepark_result]
        address_string = '|'.join(address_list)
        a = time.time()
        desp = gmaps.distance_matrix(origins=f'{latitude}, {longitude}',
                                     destinations=address_string,
                                     transit_mode='driving')
        print(skatepark_result[0]['name'])
        names = [park['name'] for park in skatepark_result]
        destinations = desp['destination_addresses']
        durations = [
            element['duration'] for element in desp['rows'][0]['elements']
        ]
        distances = [
            element['distance'] for element in desp['rows'][0]['elements']
        ]
        dest_info = build_destination(names, destinations, distances, durations)
        parks = list(make_parks(dest_info))
        # for park in parks:
        #     print(park, end='\n')
        print(f'\n\n\nExec time: {time.time() - a}\n\n\n\n')
        return render_template('results.html', form=form, results=parks, origin=city)

    #     for park in skatepark_result:
    #         b = time.time()
    #         address = park['formatted_address']
    #         distance_response = gmaps.distance_matrix(origins=f'{latitude}, {longitude}', destinations=address, transit_mode='driving')
    #         distance = distance_response['rows'][0]['elements'][0]['distance']['text']
    #         duration = distance_response['rows'][0]['elements'][0]['duration']['text']

    #         # retrieve photo url (some don't have photos)
    #         try:
    #             for photo in park['photos']:
    #                 reference = photo['photo_reference']
    #                 photo_url = requests.get(default_url + 'maxwidth=' + width +'&photoreference=' + reference + '&key=' + API_KEY).url
    #         except Exception as e:
    #             print(f'{e}')

    #         entry = Result(origin=city,
    #                         name=park['name'],
    #                         address=park['formatted_address'],
    #                         rating=park['rating'],
    #                         distance=distance,
    #                         duration=duration,
    #                         photo=photo_url)
    #         places_results.append(entry)
    #         print(city, park['name'], address, park['rating'], distance, duration, photo_url)
    #         print(f'speed = {time.time() - b}')
        # db_reset()
        # db.session.add_all(places_results)
        # db.session.commit()

    # # pagination
    # page = request.args.get('page', 1, type=int)
    # page_results = Result.query.order_by(Result.duration.asc()).paginate(page=page, per_page=5)

    # print(f'Finished: Exec time = {time.time() - start}')

    # return render_template('results.html', form=form, results=page_results, origin=city)
    # return 'CONSTRUCTION'


# sort by routes
@app.route('/rate_high', methods=['GET', 'POST'])
def rate_high():
    city = Result.query.with_entities(Result.origin).limit(1).scalar()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.rating.desc()).paginate(
        page=page, per_page=5)
    return render_template('rate_high.html', results=page_results, origin=city)


@app.route('/rate_low', methods=['GET', 'POST'])
def rate_low():
    city = Result.query.with_entities(Result.origin).limit(1).scalar()
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.rating.asc()).paginate(
        page=page, per_page=5)
    return render_template('rate_low.html',
                           form=form,
                           results=page_results,
                           origin=city)


@app.route('/time_fast', methods=['GET', 'POST'])
def time_fast():
    city = Result.query.with_entities(Result.origin).limit(1).scalar()
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.duration.asc()).paginate(
        page=page, per_page=5)
    return render_template('time_fast.html',
                           form=form,
                           results=page_results,
                           origin=city)


@app.route('/time_slow', methods=['GET', 'POST'])
def time_slow():
    city = Result.query.with_entities(Result.origin).limit(1).scalar()
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.duration.desc()).paginate(
        page=page, per_page=5)
    return render_template('time_slow.html',
                           form=form,
                           results=page_results,
                           origin=city)
