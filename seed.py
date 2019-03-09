from model import User, Contact, Phone, Alert, NaturalDisaster, Location, Earthquake, UserSetting, Setting, connect_to_db, db
from server import app

import os


TEST_PHONE = os.environ.get('TEST_PHONE')
#TODO: Add a second verified number to be able to test

#CREATE USERS
user_fabio = User(name="Fabio", age=45, email="f@email.com", password="123", residency_address="599 Manor St. Villa Rica, GA 30180", zipcode="30180",
            phone="14156783456", allergies="Penicillin, lactose, dogs", medications="Metformin, Amlodipine")

user_juan = User(name="Juan", age=26, email="j@email.com", password="456", residency_address="155 Valley View Court Roslindale, MA", zipcode="02131",
            phone="14155389463", allergies="Aspirin, seafood, nuts, cats", medications="Lipitor, Lisinopril")

#CREATE SETTINGS
eq_mag_setting = Setting("eqmag", "Earthquake magnitude alert level")

fabio_mag_setting = UserSetting(setting=eq_mag_setting,
                                user_value="4.5")

juan_mag_setting = UserSetting(setting=eq_mag_setting,
                                user_value="2.5")

user_fabio.user_settings.append(fabio_mag_setting)

user_juan.user_settings.append(juan_mag_setting)

#CREATE LOCATION

location1 = Location(lat=37.776460, lng=-122.228150, address="3098 E 10th St, Oakland, CA 94601")
user_fabio.locations.append(location1)

location2 = Location(lat=37.787970, lng=-122.418470, address="683 Sutter St, San Francisco, CA 94109")
user_juan.locations.append(location2)


#CREATE PHONES
home_jesus = Phone(phone=TEST_PHONE, type="home")
cel_jesus = Phone(phone=TEST_PHONE, type="cel")

cel_nati = Phone(phone=TEST_PHONE, type="cel")
home_nati = Phone(phone=TEST_PHONE, type="home")


#CREATE CONTACTS
nati_contact = Contact(name="Nati")
nati_contact.user = user_fabio
nati_contact.phones.extend([cel_nati, home_nati])

marco_contact = Contact(name="Marco")
marco_contact.user = user_fabio

jesus_contact = Contact(name="Jesus")
jesus_contact.user = user_juan
jesus_contact.phones.extend([cel_jesus, home_jesus])


#CREATE NATURAL DISASTERS & ALERTS
natural_disaster_1 = NaturalDisaster(nat_type="Earthquake", title="Earthquake- M 4.6 - 21km SSE of Kettleman City, CA", latitude="37.689511", longitude="-122.468796", location="4km WSW of Daly City, CA", timestamp="2019-02-12 15:08:40 (UTC)")
alert_1 = Alert(natural_disaster=natural_disaster_1,
                message="Earthquake- M 4.6 - 21km SSE of Kettleman City, CA ******* User Location: 3098 E 10th St, Oakland, CA 94601 - User Coordinates (lat,lng): 37.776460, -122.228150 - Allergies: Penicillin, lactose, dogs - Medications: Metformin, Amlodipine")
alert_1.user = user_fabio

natural_disaster_2 = NaturalDisaster(nat_type="Earthquake", title="Earthquake- M 5.8 - 4km WSW of Daly City, CA", latitude="36.008795", longitude="-119.962860", location="21km SSE of Kettleman City, CA", timestamp="2019-05-8 03:03:30 (UTC)")
alert_2 = Alert(natural_disaster=natural_disaster_2,
                message="Earthquake- M 5.8 - 4km WSW of Daly City, CA ******** User Location: 683 Sutter St, San Francisco, CA 94109 - User Coordinates (lat,lng): 37.787970, -122.418470 - Allergies: Aspirin, seafood, nuts, cats - Medications: Lipitor, Lisinopril")
alert_2.user = user_juan


#CREATE EARTHQUAKES
earthquake_1 = Earthquake(magnitude=4.6)
earthquake_1.natural_disaster = natural_disaster_1

earthquake_2 = Earthquake(magnitude=5.8)
earthquake_2.natural_disaster = natural_disaster_2


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    #COMMIT USERS
    db.session.add_all([user_fabio, user_juan])
    db.session.commit()

    #COMMIT PHONES
    db.session.add_all([home_jesus, cel_jesus, cel_nati, home_nati])
    db.session.commit()

    #COMMIT CONTACTS
    db.session.add_all([nati_contact, marco_contact, jesus_contact])
    db.session.commit()

    #COMMIT NATURAL DISASTERS
    db.session.add_all([natural_disaster_1, natural_disaster_2])
    db.session.commit()

    #COMMIT EARTHQUAKES
    db.session.add_all([earthquake_1, earthquake_2])
    db.session.commit()

    #COMMIT ALERTS
    db.session.add_all([alert_1, alert_2])
    db.session.commit()
