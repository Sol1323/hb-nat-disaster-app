"""Natural Disaster Alert App."""

from pprint import pformat
import os

# import requests
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Contact, Phone, Alert, Natural_Disaster, Earthquake, connect_to_db, db

#Uncomment later when model defined
# from model import connect_to_db, db, User, Contact, Alert, Natural_Disaster


app = Flask(__name__)

#Get secret key for DebugToolbarExtension
app.secret_key = os.environ.get('APP_SECRET_KEY')

# TODO: Fix this to raise an error.
# Normally, if you use an undefined variable in Jinja2, it fails silently.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""

    return render_template("index.html")

@app.route('/signup', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("signup_form.html")


@app.route('/signup', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    name = request.form["name"]
    phone = request.form["phone"]
    zipcode = request.form["zipcode"]
    medications = request.form["medications"]
    allergies = request.form["allergies"]

    new_user = User(email=email,
                    password=password,
                    name=name,
                    phone=phone,
                    zipcode=zipcode,
                    medications=medications,
                    allergies=allergies
                    )

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {name} added.")
    return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
