# parks.py - this python script will be used to locate skateparks within a 25 mile radius

import googlemaps, pprint, time, json, sys, os
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


API_KEY = os.environ.get('API_KEY')
gmaps = googlemaps.Client(key=API_KEY)
query = ['skatepark', 'skate park']
skatepark_result = gmaps.places(query=query[0] or query[1], radius=40000, location=f'{latitude}, {longitude}')


def park_info():
    ''' prints the name of the skatepark and the rating '''
    n = '\n'
    for park in skatepark_result['results']:
        my_place_id = park['place_id']
        my_fields = ['name', 'rating', 'vicinity']
        park_details = gmaps.place(place_id=my_place_id, fields=my_fields)

        print(f"Name: {park_details['result']['name']} Rating: {park_details['result']['rating']}{n}Address: {park_details['result']['vicinity']}{n}")


def pic_reference():
    ''' get picture reference and name and place it in dictionary'''
    ref = {}
    for park in skatepark_result['results']:
        name = park['name']
        for photo in park['photos']:
            reference = photo['photo_reference']
            ref.update({name: reference})
    return ref


def download_photo():
    ''' download photos of skatepark in folder of current working directory using the photo reference '''
    os.makedirs('Photos', exist_ok=True)
    for name, photo_ref in pic_reference().items(): 
        print(f'Checking if picture of {name} exists  . . . ')

        if not os.path.exists(os.path.join('Photos/' + name)):
            print(f'Beginning to download {name} . . .')
            for i in range(len(pic_reference())):
                    f = open(os.path.join('Photos', name), 'wb')
                    for chunk in gmaps.places_photo(photo_ref, max_width=300):
                        if chunk:
                            f.write(chunk)
                    f.close()
            print(f'Finished downloading picture of {name} . . . \n')

        else: 
            print(f'{name} already exists . . . Checking next park . . . \n')


def main(): 
    park_info()
    pic_reference()
    download_photo()


if __name__ == '__main__':
    main()

# TODO: figure out how calculate the distance between the parks to the user's city