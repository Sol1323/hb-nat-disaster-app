"""Models and database functions for Natural Disaster project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of natural disaster alerts system"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    name = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    residency_address = db.Column(db.String(450), nullable=True)
    zipcode = db.Column(db.String(20), nullable=True)
    allergies = db.Column(db.String(250), nullable=True)
    medications = db.Column(db.String(250), nullable=True)
    phone = db.Column(db.String(64), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} name={self.name} email={self.email}>"


class Contact(db.Model):
    """Contact from user for alert system"""

    __tablename__ = "contacts"

    contact_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'))
    name = db.Column(db.String(64), nullable=True)


    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("contacts"))

    # Define relationship to phone
    phones = db.relationship("Phone",
                            backref=db.backref("contact"))  # type: Phone[]

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Contact contact_id={self.contact_id} name={self.name} user_id={self.user_id} phone_id={self.phone_id}>"


class Phone(db.Model):
    """Phone from contact for alert system"""

    __tablename__ = "phones"

    phone_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)

    phone = db.Column(db.String(64), nullable=True)
    contact_id = db.Column(db.Integer,
                            db.ForeignKey("contacts.contact_id"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Phone phone_id={self.phone_id} phone={self.phone}>"


class Alert(db.Model):
    """Alert contacts in alert system"""

    __tablename__ = "alerts"

    alert_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'))
    nat_id = db.Column(db.Integer,
                         db.ForeignKey('natural_disasters.nat_id'))
    message = db.Column(db.String(650), nullable=True)

    #Define relationship to natural disaster
    natural_disaster = db.relationship("NaturalDisaster",
                                        uselist=False)

    #Define relationship to users
    user = db.relationship("User",
                            uselist=False)

    #TODO: Draft of init method. Watch how to instantiate a message using instance attibutes.
    # def __init__(self, user, nat):  # Alert(juan, natural_disaster_1)
    #     self.user = user
    #     # etc
    #
    #     self.message = f"{user.medications}"


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Alert alert_id={self.alert_id} user_id={self.user_id} nat_id={self.nat_id} message={self.message}>"


class NaturalDisaster(db.Model):
    """Natural Disaster in alert system"""

    __tablename__ = "natural_disasters"

    nat_id = db.Column(db.Integer,
                        autoincrement=True,
                         primary_key=True)
    nat_type = db.Column(db.String(20))
    latitude = db.Column(db.String(250))
    longitude = db.Column(db.String(250))
    location = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime)

    earthquake = db.relationship("Earthquake",
                                    uselist=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<NaturalDisaster nat_id={self.nat_id} nat_type={self.nat_type} location={self.location} timestamp={self.timestamp}>"


class Earthquake(db.Model):
    """Earthquake in alert system"""

    __tablename__ = "earthquakes"

    nat_id = db.Column(db.Integer,
                        db.ForeignKey("natural_disasters.nat_id"),
                         primary_key=True)
    magnitude = db.Column(db.Integer)

    natural_disaster = db.relationship("NaturalDisaster",
                                        uselist=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Earthquake earthquake_id={self.earthquake_id} magnitude={self.magnitude}>"



#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///natdis'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
