from model import User, Contact, Phone, Alert, NaturalDisaster, Earthquake, UserSetting, Setting, connect_to_db, db
from server import app



#CREATE USERS
user_fabio = User(name="Fabio", age=45, email="f@email.com", password="123",
            phone="893829987", allergies="penicilina", medications="insulin")

user_juan = User(name="Juan", age=26, email="j@email.com", password="456",
            phone="12345678", allergies="seafood", medications="lorazepan")

#CREATE SETTINGS
eq_mag_setting = Setting("eqmag", "Earthquake magnitude alert level")

fabio_mag_setting = UserSetting(setting=eq_mag_setting,
                                user_value="4.5")

user_fabio.user_settings.append(fabio_mag_setting)
#TODO: check how to add a new user setting


#CREATE PHONES
home_jesus = Phone(phone="1234567", type="home")
cel_jesus = Phone(phone="13445654", type="cel")

cel_nati = Phone(phone="3453546", type="cel")
home_nati = Phone(phone="54657687", type="home")


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
natural_disaster_1 = NaturalDisaster(title="Earthquake- M 4.6 - 21km SSE of Kettleman City, CA", latitude="37.676", longitude="122.509", location="4km WSW of Daly City, CA", timestamp="2019-02-12 15:08:40 (UTC)")
alert_1 = Alert(natural_disaster=natural_disaster_1,
                message="Earthquake- M 4.6 - 21km SSE of Kettleman City, CA ******* User Location: 4355 Cornova st. Andaman and Nicobar Islands 744107, India User Coordinates: 35.839°N 119.849°W - Medical Information: allergies=seafood, medication=lorazepan")
alert_1.user = user_fabio

natural_disaster_2 = NaturalDisaster(title="Earthquake- M 5.8 - 4km WSW of Daly City, CA", latitude="35.839", longitude="119.849", location="21km SSE of Kettleman City, CA", timestamp="2019-05-8 03:03:30 (UTC)")
alert_2 = Alert(natural_disaster=natural_disaster_2,
                message="Earthquake- M 5.8 - 4km WSW of Daly City, CA ******** User Location: 310 Magnolia st. Daly City, CA - User Coordinates: 37.676°N 122.509°W - Medical Information: allergies=penicilina, medication=insulin")
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
