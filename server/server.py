import random
import os
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__, static_folder='../static/dist', template_folder='../static')

#Get secret key for DebugToolbarExtension
app.secret_key = os.environ.get('APP_SECRET_KEY')



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello') # take note of this decorator syntax, it's a common pattern
def hello():
    # It is good practice to only call a function in your route end-point,
    # rather than have actual implementation code here.
    # This allows for easier unit and integration testing of your functions.
    return get_hello()


def get_hello():
    greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej']
    return random.choice(greeting_list)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
