"""Natural Disaster Alert App."""

from pprint import pformat
import os

# import requests
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Contact, Phone, Alert, NaturalDisaster, Earthquake, connect_to_db, db


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
def signup_form():
    """Show form for user signup."""

    return render_template("signup_form.html")


@app.route('/signup', methods=['POST'])
def signup_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    name = request.form["name"]
    age = int(request.form["age"])
    phone = request.form["phone"]
    residency_address=request.form["residency-address"]
    zipcode = request.form["zipcode"]
    medications = request.form["medications"]
    allergies = request.form["allergies"]

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
    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Oops! Email or password wrong. Please retry again.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash(f"{user.name} successfully logged in!")
    return redirect(f"/users/{user.user_id}")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


@app.route('/add-contact', methods=['POST'])
def add_contact():
    """Add a contact into the database."""

    print(f"\n\nRequest: POST {request.url}\n\n")

    # Get form variables
    name = request.form.get("name")
    type = request.form.get("type")
    phone = request.form.get("phone")

    user_id = session.get("user_id")

    new_contact = Contact(name=name, user_id=user_id)
    # new_contact.phones.append(phone)
    # new_contact.phones.type = type

    db.session.add(new_contact)
    db.session.commit()

    flash(f"Contact {name} added.")
    return "your contact has been added"


@app.route('/contacts', methods=['GET'])
def contact_list():
    """Show list of all contacts."""

    contacts = Contact.query.all()
    return render_template("contact_list.html", contacts=contacts)


@app.route('/contacts/<int:contact_id>')
def contact_detail(contact_id):
    """Show info about contact."""

    contact = Contact.query.get(contact_id)
    return render_template("contact.html", contact=contact)


@app.route('/earthquakes', methods=['GET'])
def earthquake_list():
    """Show list of all earthquakes."""

    earthquakes = Earthquake.query.all()
    return render_template("earthquake_list.html", earthquakes=earthquakes)


@app.route('/earthquakes/<int:nat_id>')
def earthquake_detail(nat_id):
    """Show info about an earthquake."""

    earthquake = Earthquake.query.get(nat_id)
    return render_template("earthquake.html", earthquake=earthquake)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
