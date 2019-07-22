from website import db
from website.main import geolocator, gmaps
from website.classes.Park import Park
from flask import request

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

def get_form_details() -> dict:
    results = request.form
    location = results['location']
    search_radius = miles_to_meters(results['radius']) 
    return {"location": location, "radius": search_radius}

def get_geo(results) -> dict:
    geolocation = geolocator.geocode(results['location'])
    geolat = geolocation.latitude
    geolong = geolocation.longitude
    return {"geolocation" : geolocation, "geolat" : geolat, "geolong" : geolong}

def gmaps_query(query: str) -> dict:
    pass