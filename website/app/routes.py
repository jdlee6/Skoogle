from flask import redirect, url_for, render_template, request, abort
import googlemaps, json, os, requests
from app.forms import SearchForm
from geopy.geocoders import Nominatim
from app import app, API_KEY, db
from app.models import Result
from app.classes.Park import Park
import time, asyncio, aiohttp


gmaps = googlemaps.Client(key=API_KEY)
query = ['skatepark', 'skate park']
default_url = 'https://maps.googleapis.com/maps/api/place/photo?'
height = "1000"


def db_reset():
    db.drop_all()
    db.create_all()


def build_destination(names, destinations, ratings, distances, durations, photo_url):
    return list(zip(names, destinations, ratings, distances, durations, photo_url))


def make_parks(data):
    return (Park(x) for x in data)


def miles_to_meters(miles):
    return int(float(miles)*1609.344)


def seconds_to_minutes(seconds):
    return int(seconds / 60)


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    return render_template('home.html', form=form)


@app.route('/results', methods=['GET', 'POST'])
def results():
    form = SearchForm()
    if form.validate_on_submit():
        geolocator = Nominatim(user_agent="myapplication")
        DISTANCE_RADIUS = miles_to_meters(form.radius.data)
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
        names = [park['name'] for park in skatepark_result]
        ratings = [park['rating'] for park in skatepark_result]
        destinations = desp['destination_addresses']
        durations = [
            element['duration'] for element in desp['rows'][0]['elements']
        ]
        distances = [
            element['distance'] for element in desp['rows'][0]['elements']
        ]

        photo_list = []
        async def fetch():
            try:
                async with aiohttp.ClientSession() as session:
                    for park in skatepark_result:
                        for photo in park['photos']:
                            reference = photo['photo_reference']
                            async with session.get(default_url + 'maxheight=' + height +'&photoreference=' + reference + '&key=' + API_KEY) as response:
                                # parses yarl URL object to retrieve the string only and then appends it to photo_list
                                photo_list.append(str(response.url))
            except Exception as e:
                print(f'Error! Missing Photo')
        
        asyncio.run(fetch())

        print(city, names, destinations, ratings, durations, distances, photo_list)
        dest_info = build_destination(names, destinations, ratings, distances, durations, photo_list)
        parks = list(make_parks(dest_info))

        # adding to park instance attributes to database
        db_reset()
        for park in parks:
            entry = Result(city=city,
                    name=park.name,
                    address=park.destination,
                    rating=park.rating,
                    distance=park.distance,
                    duration=seconds_to_minutes(park.duration),
                    photo_url=park.photo_url)
            db.session.add(entry)
            db.session.commit()
            
        print(f'speed = {time.time() - a}')    
        if request.method == 'GET':
            page = request.args.get('page', type=int)
            radius = request.form.get('radius')
            return redirect(url_for('results', page=page, radius=radius))

    # pagination
    page = request.args.get('page', 1, type=int)
    radius = request.form.get('radius')
    page_results = Result.query.paginate(page=page, per_page=2)

    return render_template('results.html', form=form, results=page_results, origin=city, radius=radius)


# sort by routes
@app.route('/rate_high', methods=['GET', 'POST'])
def rate_high():
    city = Result.query.with_entities(Result.city).limit(1).scalar()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.rating.desc())\
                                                .paginate(page=page, per_page=2)
    return render_template('rate_high.html', results=page_results, origin=city)


@app.route('/rate_low', methods=['GET', 'POST'])
def rate_low():
    city = Result.query.with_entities(Result.city).limit(1).scalar()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.rating.asc())\
                                                .paginate(page=page, per_page=2)
    return render_template('rate_low.html',
                           results=page_results,
                           origin=city)


@app.route('/time_fast', methods=['GET', 'POST'])
def time_fast():
    city = Result.query.with_entities(Result.city).limit(1).scalar()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.duration.asc())\
                                                .paginate(page=page, per_page=2)
    return render_template('time_fast.html',
                           results=page_results,
                           origin=city)


@app.route('/time_slow', methods=['GET', 'POST'])
def time_slow():
    city = Result.query.with_entities(Result.city).limit(1).scalar()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.duration.desc())\
                                                .paginate(page=page, per_page=2)
    return render_template('time_slow.html',
                           results=page_results,
                           origin=city)


# Error Handling


@app.errorhandler(403)
def error_403(error):
    return render_template('/errors/403.html'), 403


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500