from flask import Flask, redirect, url_for, render_template
import googlemaps, json, sys, os, requests
from forms import SearchForm
from geopy.geocoders import Nominatim

API_KEY = os.environ.get('API_KEY')
gmaps = googlemaps.Client(key=API_KEY)
query = ['skatepark', 'skate park']
url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
# mode can be driving, walking, bicycling or transit (pub transportation)
mode = 'driving'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

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

    ''' need to fix here - only displaying distance for one park instead of every single park '''
    for park in skatepark_result['results']:
        address = park['formatted_address']
        # print(address)
        distance_response = dict(requests.get(url + 'origins= ' + city + '&destinations=' + address +  '&mode=' + mode + '&key= '+ API_KEY).json())
        list_of_distances.append(distance_response['rows'][0]['elements'][0]['distance']['text'])
        list_of_durations.append(distance_response['rows'][0]['elements'][0]['duration']['text'])
        # print(distance_response)
        # temp = load_d.copy()
        # load_d = {**temp, **distance_response}
        # load_d_before = distance_response
    # print(list_of_distances)    
    load_d = list(zip(list_of_distances, list_of_durations))
    index = 0
    for parks in load_r:
        parks['distance'] = load_d[index][0]
        parks['duration'] = load_d[index][1]
        index += 1

    # print(load_r)

    # right here, load_d has last reference from the for loop ^^^
    return render_template('results.html', form=form, response=load_r)


    ''' distance matrix api call - need to somehow extract the addresses in the html template when it iterates through the park and request them through this url call'''







        # retrieve the km portion and duration from distance matrix api
        # try:
        # for i in data['rows']:
        #     element = i['elements']
        #     for j in element:
        #         distance = j['distance']['text']
        #         duration = j['duration']['text']
        # except Exception as e:
        #     print(f'Unavailable: {e}')

if __name__ == "__main__":
    app.run(debug=True)

# from app import routes