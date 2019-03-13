from quakefeeds import QuakeFeed
import schedule
import time
import os
# from server import session, client, TEST_PHONE
# from twilio.rest import Client
from geopy import distance
from twilio.rest import Client
# from flask import flash
# from flask import Flask, render_template, request, flash, redirect, session, jsonify
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
client = Client(TWILIO_TEST_SID, TWILIO_TEST_TOKEN)
# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)



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
    title = feed.event_title(idx) #Ex. 'USGS Magnitude 4.5+ Earthquakes, Past Day'

    #Get magnitude of the earthquake
    magnitude = feed.magnitude(idx)

    #Get location coordinates
    coordinates = feed.location(idx)
    longitude = str(coordinates[0])
    latitude = str(coordinates[1])

    #Get place description
    location = feed.place(idx)

    #This will give us the time in format
    timestamp = feed.event_time(idx) #Ex. datetime.datetime(2015, 4, 16, 19, 18, 39, tzinfo=datetime.timezone.utc)


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

    # Geopy can calculate geodesic distance between two points using the geodesic distance
    # https://pypi.org/project/geopy/
    diff_distance = distance.distance(user_location, eq_location).miles

    if diff_distance < 400:

        return True

    # If user.user_settings is 4.5 or higher then it can be felt from far away < 400
    # If user.user_settings is lower than 4.5 then it can be felt from closer distance 100
    #Make a query of all settings with joinedload to not have lazyloading
    # settings = UserSetting.query.options(db.joinedload('user')).all()

    #TODO: Get all users that match eq mag
    # for setting in settings:
    #     user_value = float(setting.user_value)
    #     if magnitude >= user_value:

def send_sms(phone, user, body):
    # for contact in contacs:
    message = client.messages \
                    .create(
                         body=body,
                         from_=TEST_FROM_PHONE, #change to TEST_FROM_PHONE
                         to=phone #contact for testing just direct phone number
                     )

    print("\n\n\n")
    print("This is the message sid:",message.sid)
    print("\n\n\n")

def get_new_earthquake(level, period):
    """Get most recent earthquake object"""

    #TEST WITH DATABASE EARTHQUAKE FROM CA
    ca_eq = NaturalDisaster.query.get(1)
    magnitude = ca_eq.earthquake.magnitude
    lat_test = float(ca_eq.latitude)
    lng_test = float(ca_eq.longitude)
    test_eq_coord = (lat_test, lng_test)

    new_earthquake = None

    last_feed = get_all_earthquakes(level, period) #Quake feed object
    print("Last feed element zero is: ", last_feed[0])
    new_feed = get_all_earthquakes(level, period)


    if last_feed:
        last_feed_time = get_ms_time(last_feed, 0)
        new_feed_time = get_ms_time(new_feed, 0)

        #Until they are not equal keep requesting but last_feed will remain the same
        while last_feed_time == new_feed_time:
            new_feed = get_all_earthquakes(level, period)
            new_feed_time = get_ms_time(new_feed, 0)
            # new_feed_time = "dsjifhdfh" for testing feed
            print("last feed made:", last_feed)
            print("new request made:", new_feed)

        #Get new_earthquake in the new_feed request
        new_earthquake_feed = new_feed
        eq_location = get_coords(new_earthquake_feed, 0) #(lat,lng)
        magnitude = new_earthquake_feed.magnitude(0)
        #Make a query of all locations with joinedload to not have lazyloading
        locations = Location.query.options(db.joinedload('user')
                                             .joinedload('contacts')
                                             .joinedload('phones')).all()

        #Iterate over all locations to see if there is someone close to the new_earthquake
        for location in locations:

            user_location = (location.lat, location.lng)

            #Calculate geodesic distance between both user and new_earthquake location
            is_near = calculate_distance(user_location, eq_location) #change to test_eq_coord for testing

            #Check if it is near to send sms
            if is_near:
                #Get user & user contacts
                user = location.user
                user_contacts = user.contacts
                #Save the earthquake into db
                natural_disaster = add_earthquake_to_db(new_earthquake_feed)

                #Iterate over all contacts to get all phones
                for contact in user_contacts:
                    #Get all phones of the contact
                    phones = contact.phones #type:[]
                    #Iterate over the phones to send sms
                    for phone in phones:
                        body = user.create_message(natural_disaster) #change to ca_eq for testing
                        phone = phone.phone

                        send_sms(phone, user, body)
                #Send a confirmation to user that a message has been sent to all of his contacts and of the event
                body = user.create_confirmation_message(natural_disaster)
                phone = user.phone
                send_sms(phone, user, body)


if __name__ == '__main__':
#
    connect_to_db(app)
#     # schedule.every(1).seconds.do(get_new_earthquake, level="all", period="hour")
#     #
#     schedule.run_continuously(1)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
