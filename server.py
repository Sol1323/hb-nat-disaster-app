"""Natural Disaster Alert App."""

import json
import os
import schedule
from quake import *
# from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
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
#Get twilio account sid, auth token, phone number for sms
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

# Account SID and Auth Token for twilio
client = Client('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN')


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
@app.route('/settings/setting_code', methods=['POST'])
def update_setting(setting_code):
    """Add a contact into the database."""

    #TODO: Finish this route.
    #Get form variables
    magnitude = request.form.get("magnitude")


    user_id = session.get("user_id")

    eq_mag_setting = Setting(setting_code, "Earthquake magnitude alert level")
    new_setting = UserSetting(user_value=magnitude, user_id=user_id, setting=eq_mag_setting)

    db.session.add(new_setting)
    db.session.commit()


    flash(f"Setting added.")

    return jsonify(new_setting.convert_to_dict())


#----------------------------SMS ROUTES---------------------------------------

@app.route('/alerts')
def create_alerts():
    """Create an sms alert to user's contacts."""

    user_id = session['user_id']
    user = User.query.get(user_id)
    user_contacts = None

    # Grab the relevant phone numbers.
    #TODO: Modify to alert multiple phone numbers
    to_number = request.form['To']

    lat = request.args.get("lat")
    lng = request.args.get("lng")

    print("\n\n\n")
    print("LAT", lat)
    print("LNG", lng)

    message = client.messages \
                    .create(
                         body=f"{user.name} location is {lat} {lng}. The person is in an earthquake.",
                         from_=TWILIO_PHONE_NUMBER,
                         to=user_contacts
                     )

    print(message.sid)

    return redirect(f'/users/{user.user_id}')
    # return str(response)



if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    # schedule.run_continuously(1)
    # schedule.every(5).seconds.do(get_new_earthquake, level="all", period="hour")
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    app.run(host='0.0.0.0')
