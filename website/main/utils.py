from website import db
from website.classes.Park import Park


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