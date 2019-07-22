from flask import Blueprint, redirect, url_for, render_template, request, abort, Flask
from flask import current_app
from website import db
from website.main.forms import SearchForm
from website.main.utils import db_reset, build_destination, make_parks, miles_to_meters, seconds_to_minutes, get_form_details, get_geo
from website.models import Result
from website.main import gmaps
import json, os, requests
import time, asyncio, aiohttp

# create instance of Blueprint; 'main' is the name
main = Blueprint('main', __name__)


# home route
@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    return render_template('home.html', form=form)


# results route
@main.route('/results', methods=['GET', 'POST'])
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
        query = ['skatepark', 'skate park']
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

        # build up photo_list to be added to Park object
        photo_list = []
        for park in skatepark_result:
            print(park)
            try:
                for photo in park['photos']:
                    reference = photo['photo_reference']
                    photo_url = current_app.config['GPHOTO_URL'] + 'maxheight=' + current_app.config['PHOTO_HEIGHT'] +'&photoreference=' + reference + '&key=' + current_app.config['API_KEY']
                    photo_list.append(photo_url)
            except Exception as e:
                print(f'caught exeption {e}')

        async def fetch(url):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    pass

        # create loop and then run it in another thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [loop.create_task(fetch(photo_url))]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

        # print(city, names, destinations, ratings, durations, distances, photo_list)
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
            return redirect(url_for('main.results', page=page, radius=radius))
        
    # pagination
    page = request.args.get('page', 1, type=int)
    radius = request.form.get('radius')
    page_results = Result.query.paginate(page=page, per_page=2)
    print(page_results)

    return render_template('results.html', form=form, results=page_results, origin=city, radius=radius)


@main.route('/results2', methods=['GET', 'POST'])
def results2():
    if request.method == 'POST':
        print(f'\n*-*-*-* Post Method Received in Results *-*-*-*\n')
        results = get_form_details()
        geo = get_geo(results)
        print(f"\n*-*-*-* location = {results['location']} -- search radius = {results['radius']} -- geolocation = {geo['geolocation']} *-*-*-*)\n")
        print(f"{geo['geolat']} {geo['geolong']}")





    return  'Hi'