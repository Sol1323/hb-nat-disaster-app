"""Natural Disaster Alert App."""

from pprint import pformat
import os

# import requests
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

#Uncomment later when model defined
# from model import connect_to_db, db, User, Contact, Alert, Natural_Disaster


app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ.get('APP_SECRET_KEY')



# TODO: Fix this to raise an error.
# Normally, if you use an undefined variable in Jinja2, it fails silently.
app.jinja_env.undefined = StrictUndefined



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
