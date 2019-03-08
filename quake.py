from quakefeeds import QuakeFeed
import schedule
import time
import os
# from server import session, client, TEST_PHONE
# from twilio.rest import Client
from geopy import distance
from twilio.rest import Client
from flask import flash
# from flask import Flask, render_template, request, flash, redirect, session, jsonify
from model import NaturalDisaster, Earthquake, User

#Get twilio account sid, auth token, phone number for sms and test phones
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
TWILIO_TEST_TOKEN = os.environ.get('TWILIO_TEST_TOKEN')
TWILIO_TEST_SID = os.environ.get('TWILIO_TEST_SID')
TEST_PHONE = os.environ.get('TEST_PHONE')

# Account SID and Auth Token for twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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


def create_earthquake_for_db(feed, idx=0):
    """Save earthquake into database using feed methods to get data"""

    nat_type = "earthquake"
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

    return earthquake


def get_new_earthquake(level, period):
    """Get most recent earthquake object"""

    new_earthquake = None

    last_feed = get_all_earthquakes(level, period) #Quake feed object
    print("Last feed element zero is: ", last_feed[0])
    new_feed = get_all_earthquakes(level, period)


    if last_feed:
        last_feed_time = get_ms_time(last_feed, 0)
        new_feed_time = get_ms_time(new_feed, 0)

        while last_feed_time == new_feed_time:
            #until they are not equal keep requesting
            new_feed = get_all_earthquakes(level, period)
            new_feed_time = get_ms_time(new_feed, 0)


        #once new feed is different we will output new_earthquake
        new_earthquake_feed = new_feed
        eq_location = get_coords(new_earthquake_feed, 0) #(lat,lng)

        print("New earthquake is: ", new_earthquake_feed.event(0))
        print("New earthquake time: ", new_feed.event_time(0))

        is_near = calculate_distance(user_location, eq_location)

        if is_near:
            send_sms(TEST_PHONE)

        # return new_earthquake_feed # type: QuakeFeed obj

        #TODO: refactor code to be able to grab multiple new earthquake []
        # then append to list all the new_earthquakes
        # save_quake_into_db(new_earthquake_feed)


def calculate_distance(user_location, eq_location):

    # Geopy can calculate geodesic distance between two points using the geodesic distance
    # https://pypi.org/project/geopy/
    diff_distance = distance.distance(user_location, eq_location).miles

    if diff_distance > 400:
        # eq = create_earthquake_for_db(feed)
        # db.session.add(eq)
        # db.session.commit()
        return True
    #TODO:  instantiate alert and formulate the message
    # body = Alert(user, ca_eq, address, user_current_location)
    # If user.setting is 4.5 or higher then it can be felt from far away < 400
    # If user.setting is lower than 4.5 then it can be felt from closer distance 100
    #when committing to db make sure is not the same eq as before, make sure is not already in db


def send_sms(contacts, user):
    # for contact in contacs:
    message = client.messages \
                    .create(
                         body=f"{user.name} location is {user.locations[-1].lat} {user.locations[-1].lng}. The address is: {user.locations[-1].address} The person is in an earthquake.",
                         from_=TWILIO_PHONE_NUMBER,
                         to=contacts #contact for testing just direct phone number
                     )
    #Save message into db
    # db.session.add(body)
    # db.session.commit()

    #TODO: Modify to alert multiple phone numbers
    # contacts = user.contacts
    flash(f"Alert message sent to your contacts.")
    print("This is the message sid:",message.sid)

def get_new_earthquake(level, period):
    """Get most recent earthquake object"""

    # print(session["user_id"])

    new_earthquake = None
    # TEST WITH DATABASE EARTHQUAKE FROM CA
    # ca_eq = NaturalDisaster.query.get(1)
    # magnitude = ca_eq.earthquake.magnitude
    # lat_test = float(ca_eq.latitude)
    # lng_test = float(ca_eq.longitude)
    # test_eq_coord = (lat_test, lng_test)

    last_feed = get_all_earthquakes(level, period) #Quake feed object
    print("Last feed element zero is: ", last_feed[0])
    new_feed = get_all_earthquakes(level, period)


    if last_feed:
        last_feed_time = get_ms_time(last_feed, 0)
        new_feed_time = get_ms_time(new_feed, 0)

        while last_feed_time == new_feed_time:
            #until they are not equal keep requesting
            new_feed = get_all_earthquakes(level, period)
            new_feed_time = get_ms_time(new_feed, 0)
            # new_feed_time = "dsjifhdfh" for testing purposes
            print("new request made:", new_feed)

        new_earthquake_feed = new_feed
        eq_location = get_coords(new_earthquake_feed, 0) #(lat,lng)
        #TODO: add query for getting all users locations
        user = User.query.get(1)
        user_location = None


        if user.locations:
            user_location = (user.locations[-1].lat, user.locations[-1].lng)
            user_contacts = None #TODO: Need to get all contact numbers but for testing only using test phone

            is_near = calculate_distance(user_location, test_eq_coord)

            if is_near:
                user.create_message(ca_eq)
                print("is passing is near condition?")
                send_sms(TEST_PHONE, user) #TODO: ADD PARAM THAT PASSES IN ALL USER INFO and address

    #once new feed is different we will output new_earthquake
    # new_earthquake_feed = new_feed
    # eq_location = get_coords(new_earthquake_feed, 0) #(lat,lng)
    #
    # print("New earthquake is: ", new_earthquake_feed.event(0))
    # print("New earthquake time: ", new_feed.event_time(0))

    #QUERY DB USING USER_ID TO GET USER OBJECT
    #REAL DATA
    # user_id = session['user_id']
    # user = User.query.get(user_id)

    #COORDINATES
    # lat = session['lat']
    # lng = session['lng']
    # user_location = (lat, lng)

    #Make it a readable address
    # if lat:
    #     result = gmaps.reverse_geocode(latlng=(lat, lng))
    #     address = result[0]['formatted_address']
    #
    # print("\n\n\n")
    # print("USER_ID:", user_id)
    # print("LAT:", lat)
    # print("LNG:", lng)

# if __name__ == '__main__':
#
#
#     # schedule.every(1).seconds.do(get_new_earthquake, level="all", period="hour")
#     #
#     schedule.run_continuously(1)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
