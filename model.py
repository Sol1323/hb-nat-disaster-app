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

    __tablename__ = 'users'
    # TODO: refactor with _json_attrs
    # _json_attrs = ['email', 'password', 'name', 'age']

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

    def convert_to_dict(self):
        """Convert user into a dictionary"""

        #TODO: refactor to getattr(user, attr)
        # for attr in _json_attrs:
        #     user_dict[attr] = self.attr
        #
        # return user_dict

        user_dict = {
            'user_id': self.user_id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'age': self.age,
            'residency_address': self.residency_address,
            'zipcode' : self.zipcode,
            'allergies': self.allergies,
            'medications': self.medications,
            'phone': self.phone
        }
        return user_dict

    def add_location(self, lat, lng, address):
        location = Location(lat=lat, lng=lng, address=address)
        self.locations.append(location)

        db.session.add(self)
        db.session.commit()

    def create_message(self, natural_disaster):

        alert = Alert(nat_id=natural_disaster.nat_id,
                      user_id=self.user_id,
                      message=f"\n AlertIn:\n {self.name} location is: {self.locations[-1].address}.\n Coordinates(lat,lng): ({self.locations[-1].lat},{self.locations[-1].lng}) \n\n Age: {self.age} \n Medications: {self.medications} \n Allergies: {self.allergies} \n\n {natural_disaster.nat_type}: {natural_disaster.title} taking event at this moment."
                     )
        alert.user = self
        db.session.add(alert)
        db.session.commit()

        return alert.message

    def create_test_message(self):

        alert = Alert(user_id=self.user_id,
                      message=f"\n Welcome to AlertIn {self.name}!"
                     )
        alert.user = self
        db.session.add(alert)
        db.session.commit()

        return alert.message

    def create_confirmation_message(self, natural_disaster):

        alert = Alert(nat_id=natural_disaster.nat_id,
                      user_id=self.user_id,
                      message=f"\n AlertIn: The following message has been sent to your contacts: {self.locations[-1].address}.\n Coordinates(lat,lng): ({self.locations[-1].lat},{self.locations[-1].lng}) \n Age: {self.age} \n Medications: {self.medications} \n Allergies: {self.allergies} \n \n {natural_disaster.title} taking event at this moment."
                     )
        alert.user = self
        db.session.add(alert)
        db.session.commit()

        return alert.message


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

        return f"<Contact contact_id={self.contact_id} name={self.name} user_id={self.user_id}>"

    def convert_to_dict(self):
        """Convert contact into a dictionary"""

        phone_list = []

        for phone in self.phones:
            dict_phone = phone.convert_to_dict()
            phone_list.append(dict_phone)

        contact_dict = {
            'contact_id': self.contact_id,
            'name': self.name,
            'user': self.user.name,
            'phone': phone_list,
        }

        return contact_dict


class Phone(db.Model):
    """Phone from contact for alert system"""

    __tablename__ = 'phones'

    phone_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)

    phone = db.Column(db.String(64), nullable=True)
    type = db.Column(db.String(64), nullable=True)
    contact_id = db.Column(db.Integer,
                            db.ForeignKey('contacts.contact_id'))

    def convert_to_dict(self):

        phone_dict = {
            'phone_id': self.phone_id,
            'phone': self.phone,
            'type': self.type,
            'contact_id': self.contact_id
        }

        return phone_dict

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Phone phone_id={self.phone_id} phone={self.phone}>"


class Setting(db.Model):
    """Setting in alert system"""

    __tablename__ = 'settings'

    setting_code = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(150))


    def __init__(self, setting_code, title):
        self.setting_code = setting_code
        self.title = title

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Setting title={self.title} setting_code={self.setting_code}>"


class UserSetting(db.Model):
    """User setting in alert system"""

    __tablename__ = 'user_settings'

    user_setting_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'))
    setting_code = db.Column(db.String,
                         db.ForeignKey('settings.setting_code'))
    user_value = db.Column(db.String(250), nullable=True)

    #Define relationship to user_settings
    user = db.relationship('User',
                            backref=db.backref('user_settings'))
    #Define relationship setting
    setting = db.relationship('Setting')

    def convert_to_dict(self):
        """Convert user setting into a dictionary"""

        user_setting_dict = {
            'user_setting_id': self.user_setting_id,
            'user_id': self.user_id,
            'setting_code': self.setting_code,
            'user_value': self.user_value,
        }

        return user_setting_dict

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<UserSetting user_value={self.user_value} setting_code={self.setting_code}>"


class Alert(db.Model):
    """Alert contacts in alert system"""

    __tablename__ = 'alerts'

    alert_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'))
    nat_id = db.Column(db.Integer,
                         db.ForeignKey('natural_disasters.nat_id'))
    message = db.Column(db.String(650), nullable=True)

    #Define relationship to natural disaster
    natural_disaster = db.relationship('NaturalDisaster',
                                        uselist=False)

    #Define relationship to users
    user = db.relationship('User',
                            uselist=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Alert alert_id={self.alert_id} user_id={self.user_id} nat_id={self.nat_id} message={self.message}>"


class NaturalDisaster(db.Model):
    """Natural Disaster in alert system"""

    __tablename__ = 'natural_disasters'

    nat_id = db.Column(db.Integer,
                        autoincrement=True,
                         primary_key=True)
    nat_type = db.Column(db.String(20))
    title = db.Column(db.String(350))
    latitude = db.Column(db.String(250))
    longitude = db.Column(db.String(250))
    location = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime)

    earthquake = db.relationship('Earthquake',
                                 uselist=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<NaturalDisaster nat_id={self.nat_id} nat_type={self.nat_type} location={self.location} timestamp={self.timestamp}>"


class Earthquake(db.Model):
    """Earthquake in alert system"""

    __tablename__ = 'earthquakes'

    nat_id = db.Column(db.Integer,
                        db.ForeignKey('natural_disasters.nat_id'),
                         primary_key=True)
    magnitude = db.Column(db.Integer)

    natural_disaster = db.relationship('NaturalDisaster',
                                        uselist=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Earthquake nat_id={self.nat_id} magnitude={self.magnitude}>"


class Location(db.Model):
    """Storing location of user from Google Maps API."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(250), nullable=True)


    user = db.relationship("User",
                            backref="locations")


    def __repr__(self):

        return f"<ID={self.location_id} user_id={self.user_id} lat={self.lat} long={self.lng} address={self.address}"


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///natdis'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print('Connected to DB.')
