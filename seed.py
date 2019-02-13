
import datetime
from sqlalchemy import func

from model import User, Contact, Phone, Alert, Natural_Disaster, Earthquake, connect_to_db, db
from server import app



def create_users():

    fabio = User(name="Fabio", email="f@email.com", password="123",
                phone="893829987", allergies="penicilina", medications="insulin")

    juan = User(name="Juan", email="j@email.com", password="456",
                phone="12345678", allergies="seafood", medications="lorazepan")

    db.session.add_all([fabio, juan])
    db.session.commit()


def create_contacts():

    nati_contact = Contact(name="Nati", user_id=1)

    marco_contact = Contact(name="Marco", user_id=1)

    jesus_contact = Contact(name="Jesus", user_id=2)

    db.session.add_all([nati_contact, marco_contact, jesus_contact])
    db.session.commit()


def create_phones():

    #Jesus Phones
    home_jesus = Phone(phone="1234567")
    cel_jesus = Phone(phone="1234567")
    #Natis Phones
    cel_nati = Phone(phone="1234567")
    home_nati = Phone(phone="1234567")

    db.session.add_all([home_jesus, cel_jesus, cel_nati, home_nati])
    db.session.commit()


def create_alerts():

    alert_1 = Alert(nat_type="earthquake", user_id=2,
                    message="Earthquake- M 4.6 - 21km SSE of Kettleman City, CA ******* User Location: Bombooflat, Andaman and Nicobar Islands 744107, India User Coordinates: 35.839°N 119.849°W - Medical Information: allergies=seafood, medication=lorazepan")
    alert_2 = Alert(nat_type="earthquake", user_id=1,
                    message="Earthquake- M 5.8 - 4km WSW of Daly City, CA ******** User Location: M 2.8 - 4km WSW of Daly City, CA - User Coordinates: 37.676°N 122.509°W - Medical Information: allergies=penicilina, medication=insulin")

    db.session.add_all([alert_1, alert_2])
    db.session.commit()


def create_natural_disasters():

    natural_disaster_1 = Natural_Disaster(nat_type="earthquake", latitude="37.676", longitude="122.509", location="4km WSW of Daly City, CA", timestamp="2019-02-12 15:08:40 (UTC)")

    natural_disaster_2 = Natural_Disaster(nat_type="earthquake", latitude="35.839", longitude="119.849", location="21km SSE of Kettleman City, CA", timestamp="2019-05-8 03:03:30 (UTC)")

    db.session.add_all([natural_disaster_1, natural_disaster_2])
    db.session.commit()


def create_earthquakes():

# TODO: q1: Ask about where is the relationship between nat disas & earthquakes.
# How can we relate every natural disaster instance attributes to the specific earthquake instance

    earthquake_1 = Earthquake(magnitude=4.6, nat_type="earthquake")
    earthquake_2 = Earthquake(magnitude=5.8, nat_type="earthquake")

    db.session.add_all([earthquake_1, earthquake_2])
    db.session.commit()


#TODO: Erase when working. Please seed my database <3!
if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    #create all of the fake data
    create_users()
    create_contacts()
    create_phones()
    create_alerts()
    create_natural_disasters()
    create_earthquakes()
