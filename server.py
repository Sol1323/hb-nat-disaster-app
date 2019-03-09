"""Natural Disaster Alert App."""

import json
import os
import schedule
import googlemaps
from geopy import distance
from quake import *

# from twilio.twiml.messaging_response import MessagingResponse, Message
# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestException
# import urllib

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Contact, Phone, Alert, NaturalDisaster, Earthquake, Setting, UserSetting, connect_to_db, db


app = Flask(__name__)

#Get secret key for DebugToolbarExtension
app.secret_key = os.environ.get('APP_SECRET_KEY')
#Get google maps secret key
GOOGLE_KEY = os.environ.get('GOOGLE_KEY')

#Get twilio account sid, auth token, phone number for sms and test phones
# TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
# TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
# TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
# TWILIO_TEST_TOKEN = os.environ.get('TWILIO_TEST_TOKEN')
# TWILIO_TEST_SID = os.environ.get('TWILIO_TEST_SID')
TEST_PHONE = os.environ.get('TEST_PHONE')
#
# # Account SID and Auth Token for twilio
# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

#Define google maps client
gmaps = googlemaps.Client(GOOGLE_KEY)


# FIXME: Fix this to raise an error.
# Normally, if you use an undefined variable in Jinja2, it fails silently.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('index.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    """User sign up."""

    if request.method == 'GET':
        return render_template('signup_form.html')

    elif request.method == 'POST':
    # Get form variables
        email = request.form.get('email')
        password = request.form['password']
        name = request.form['name']
        age = int(request.form['age'])
        phone = request.form['phone']
        residency_address=request.form['residency-address']
        zipcode = request.form['zipcode']
        medications = request.form['medications']
        allergies = request.form['allergies']

        new_user = User(email=email,
                        password=password,
                        name=name,
                        age=age,
                        phone=phone,
                        residency_address=residency_address,
                        zipcode=zipcode,
                        medications=medications,
                        allergies=allergies
                        )

        db.session.add(new_user)
        db.session.commit()

        flash(f"User {name} added.")
        return redirect('/')


@app.route('/login', methods=['GET','POST'])
def login():
    """Show & process login."""

    if request.method == 'GET':
        return render_template("login_form.html")

    elif request.method == 'POST':
        # Get form variables
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Oops! Email or password wrong. Please retry again.")
            return redirect('/login')

        session['user_id'] = user.user_id

        flash(f"{user.name} successfully logged in!")
        return redirect(f'/users/{user.user_id}')


@app.route('/logout')
def logout():
    """Log out."""

    del session['user_id']
    flash('Logged Out.')
    return redirect('/')


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/<int:user_id>', methods=['POST', 'GET'])
def user_profile(user_id):
    """Get and update info about user."""

    user = User.query.get(user_id)

    if request.method == 'GET':

        return render_template('user.html', user=user, GOOGLE_KEY=GOOGLE_KEY)

    elif request.method == 'POST':
        # Get form variables
        email = request.form['email']
        name = request.form['name']
        age = int(request.form['age'])
        phone = request.form['phone']
        residency_address=request.form['residency_address']
        zipcode = request.form["zipcode"]
        medications = request.form['medications']
        allergies = request.form['allergies']

        user.email = email
        user.name = name
        user.age = age
        user.phone = phone
        user.residency_address = residency_address
        user.zipcode = zipcode
        user.medications = medications
        user.allergies = allergies

        db.session.add(user)
        db.session.commit()

        flash(f"User {name} updated.")

        return jsonify(user.convert_to_dict())


#----------------------------CONTACT ROUTES---------------------------------------
@app.route('/contacts', methods=['GET','POST'])
def contact_list():
    """Show all contacts and add a contact into the database."""

    contacts = Contact.query.all()

    if request.method == 'GET':
        return render_template('contact_list.html', contacts=contacts)

    elif request.method == 'POST':
        # Get form variables
        name = request.form.get('name')
        type = request.form.get('type')
        phone = request.form.get('phone')

        user_id = session.get('user_id')

        new_contact = Contact(name=name, user_id=user_id)
        new_phone = Phone(phone=phone, type=type)

        new_contact.phones.append(new_phone)

        db.session.add(new_contact)
        db.session.commit()


        flash(f"Contact {name} added.")

        return jsonify(new_contact.convert_to_dict())


@app.route('/contacts/<int:contact_id>', methods=['GET','POST'])
def contact_profile(contact_id):
    """Show and update info about contact."""

    contact = Contact.query.get(contact_id)

    if request.method == 'GET':
        return render_template('contact.html', contact=contact)

    elif request.method == 'POST':
        # Get form variables
        name = request.form['name']
        phone = request.form['phone']
        type = request.form['type']

        contact = Contact.query.get(contact_id)
        contact.name = name
        #FIXME: we should be modifying same phone in the idx of the list of phones
        #Maybe adding idx or converting phones to dictionary
        contact.phones[-1] = phone

        db.session.add(contact)
        db.session.commit()

        flash(f"Contact {name} updated.")

        return jsonify(contact.convert_to_dict())


#----------------------------EARTHQUAKE ROUTES---------------------------------------
@app.route('/earthquakes', methods=['GET'])
def earthquake_list():
    """Show list of all earthquakes."""

    #Get all earthquakes in the past hour
    feeds = get_all_earthquakes("all", "hour")
    earthquakes = Earthquake.query.all()
    return render_template('earthquake_list.html', earthquakes=earthquakes, feeds=feeds)


@app.route('/earthquakes/<int:nat_id>')
def earthquake_detail(nat_id):
    """Show info about an earthquake."""

    earthquake = Earthquake.query.get(nat_id)
    return render_template('earthquake.html', earthquake=earthquake)


#----------------------------SETTINGS ROUTES---------------------------------------
@app.route('/settings/<setting_code>', methods=['POST'])
def update_setting(setting_code):
    """Add a contact into the database."""

    #TODO: Finish this route.
    #Get form variables
    magnitude = request.form.get("magnitude")
    # setting = Setting.query.get("eqmag")
    # eq_mag_setting = Setting("eqmag", "Earthquake magnitude alert level")

    user_id = session.get("user_id")

    # eq_mag_setting = Setting(setting_code, "Earthquake magnitude alert level")
    new_setting = UserSetting(user_value=magnitude, user_id=user_id, setting_code=setting_code)

    db.session.add(new_setting)
    db.session.commit()


    flash(f"Setting added.")

    return jsonify(new_setting.convert_to_dict())


#----------------------------ALERT ROUTES---------------------------------------

@app.route('/locations')
def create_alerts():
    """Create an sms alert to user's contacts."""

    user_id = session['user_id']
    user = User.query.get(user_id)
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    # session['lat'] = lat
    # session['lng'] = lng

    result = gmaps.reverse_geocode(latlng=(lat, lng))
    address = result[0]['formatted_address']

    user.add_location(lat, lng, address)


    return redirect(f'/users/{user_id}')
#
#     # eq = create_earthquake_for_db(feed)
#     # db.session.add(eq)
#     # db.session.commit()
#
#
#
#     return redirect(f'/users/{user.user_id}')
    # return str(response)

#REAL DATA
# user_id = session['user_id']
#
# lat = request.args.get('lat')
# lng = request.args.get('lng')
# print(user_id)
#
# #COORDINATES
# user_location = (lat, lng)



# print("\n\n\n")
# print("LAT", lat)
# print("LNG", lng)
# print("address", address)
# print("feed:", feed)
# print("test coordinates:", test_eq_coord)
# print("test distance diff:", test_distance)


# def get_new_earthquake(level, period):
#     """Get most recent earthquake object"""
#
#     new_earthquake = None
#
#     #Instantiate two QuakeFeed objects that contain the same feed
#     last_feed = get_all_earthquakes(level, period) #Quake feed object
#     print("Last feed element zero is: ", last_feed[0])
#     new_feed = get_all_earthquakes(level, period)
#
#
#     if last_feed:
#         last_feed_time = get_ms_time(last_feed, 0)
#         new_feed_time = get_ms_time(new_feed, 0)
#
#         #Until they are not equal keep requesting but last_feed will remain the same
#         while last_feed_time == new_feed_time:
#             new_feed = get_all_earthquakes(level, period)
#             new_feed_time = get_ms_time(new_feed, 0)
#             print("New feed request made in my while loop:", new_feed)
#
#
#         #once new feed is different we will output new_earthquake
#         new_earthquake_feed = new_feed
#         eq_location = get_coords(new_earthquake_feed, 0) #(lat,lng)
#
#         print("New earthquake is: ", new_earthquake_feed.event(0))
#         print("New earthquake time: ", new_feed.event_time(0))
#
#
#         is_near = calculate_distance(user_location, eq_location)
#
#         if is_near:
#             send_sms(TEST_PHONE)

        # return new_earthquake_feed # type: QuakeFeed obj

        #TODO: refactor code to be able to grab multiple new earthquake []
        # then append to list all the new_earthquakes
        # save_quake_into_db(new_earthquake_feed)




if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    schedule.every(1).seconds.do(get_new_earthquake, level="all", period="hour")
    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    schedule.run_continuously(1)
    app.run(host='0.0.0.0')
