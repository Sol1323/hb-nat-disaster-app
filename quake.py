from quakefeeds import QuakeFeed
import schedule
import time
import os

from geopy import distance
from twilio.rest import Client

from model import NaturalDisaster, Earthquake, User, Location, UserSetting, db, connect_to_db


#Get twilio account sid, auth token, phone number for sms and test phones
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
TWILIO_TEST_TOKEN = os.environ.get('TWILIO_TEST_TOKEN')
TWILIO_TEST_SID = os.environ.get('TWILIO_TEST_SID')
TEST_PHONE = os.environ.get('TEST_PHONE')
TEST_FROM_PHONE = os.environ.get('TEST_FROM_PHONE')

# Account SID and Auth Token for twilio
# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
client = Client(TWILIO_TEST_SID, TWILIO_TEST_TOKEN)



ALLOWED_LEVELS  = { "significant", "4.5", "2.5", "1.0", "all" }
ALLOWED_PERIODS = { "hour", "day", "week", "month" }


def get_all_earthquakes(level, period):
    """Get all earthquakes denpending on magnitude and period we get a QuakeFeed object"""

    all_earthquakes = QuakeFeed(level, period)

    return all_earthquakes


def get_ms_time(feed, idx):
    """Get time from earthquake in miliseconds since the epoch"""

    time_ms = feed[idx]["properties"]["time"]

    return time_ms


def get_coords(feed, idx):
    """Get coordinates from earthquake in a tuple (lat, lng)"""

    coord = feed.location(idx)
    lng = coord[0]
    lat = coord[1]

    return (lat, lng)


def add_earthquake_to_db(feed, idx=0):
    """Save earthquake into database using feed methods to get data"""

    nat_type = "Earthquake"
    title = feed.event_title(idx)

    magnitude = feed.magnitude(idx)

    coordinates = feed.location(idx)
    longitude = str(coordinates[0])
    latitude = str(coordinates[1])

    location = feed.place(idx)

    timestamp = feed.event_time(idx)

    earthquake = Earthquake(magnitude=magnitude)

    nat_disaster = NaturalDisaster(title=title,
                                   nat_type=nat_type,
                                   latitude=latitude,
                                   longitude=longitude,
                                   location=location,
                                   timestamp=timestamp)

    earthquake.natural_disaster = nat_disaster

    db.session.add(nat_disaster)
    db.session.commit()

    return nat_disaster


def calculate_distance(user_location, eq_location):
    """Calculate geodisic distance between user and earthquake coordinates"""

    diff_distance = distance.distance(user_location, eq_location).miles

    if diff_distance < 400:

        return True


def send_sms(phone, user, body):
    """Send text message to contact's phone"""
    message = client.messages \
                    .create(
                         body=body,
                         from_=TEST_FROM_PHONE,
                         to=phone
                     )


def get_new_earthquake(level, period):
    """Get most recent earthquake object"""

    new_earthquake = None

    last_feed = get_all_earthquakes(level, period)
    new_feed = get_all_earthquakes(level, period)


    if last_feed:
        last_feed_time = get_ms_time(last_feed, 0)
        new_feed_time = get_ms_time(new_feed, 0)

        while last_feed_time == new_feed_time:
            new_feed = get_all_earthquakes(level, period)
            new_feed_time = get_ms_time(new_feed, 0)

        new_earthquake_feed = new_feed
        eq_location = get_coords(new_earthquake_feed, 0)

        magnitude = new_earthquake_feed.magnitude(0)

        locations = Location.query.options(db.joinedload('user')
                                             .joinedload('contacts')
                                             .joinedload('phones')).all()

        for location in locations:

            user_location = (location.lat, location.lng)

            is_near = calculate_distance(user_location, eq_location)

            if is_near:

                user = location.user
                user_contacts = user.contacts

                natural_disaster = add_earthquake_to_db(new_earthquake_feed)

                for contact in user_contacts:

                    phones = contact.phones #type:[]

                    for phone in phones:
                        body = user.create_message(natural_disaster)
                        phone = phone.phone

                        send_sms(phone, user, body)

                body = user.create_confirmation_message(natural_disaster)
                phone = user.phone
                send_sms(phone, user, body)


if __name__ == '__main__':

    connect_to_db(app)
