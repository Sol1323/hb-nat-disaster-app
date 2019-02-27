from quakefeeds import QuakeFeed
from model import User, Contact, Phone, Alert, NaturalDisaster, Earthquake, connect_to_db, db
from server import app


##############################  PSEUDOCODE  ################################################################
#Always getting in the past hour to get the most recent earthquakes
#magnitude will be what the user user inputs as setting
# get all settings with eq_magnitude
# get user_value for the magnitude
# pass magnitude into the QuakeFeed instance
#############################################################################################################


def get_all_earthquakes(mag):
    """Get all earthquakes denpending on magnitude string"""
    #TODO: q1->We want to get the most recent earthquakes by the hour depending on the user's value?
    feed = QuakeFeed(String(mag), "hour")

    if feed:
        for idx in range(0, len(feed)):
            title = feed.event_title(idx)
            magnitude = feed.magnitude(idx)
            timestamp = feed.event_time(idx)
            location = feed.place(idx)

            coordinates = feed.location(idx) #coord = []
            latitude = coordinates[0]
            longitude = coordinates[1]

            NaturalDisaster(title=title,
                            latitude=latitude,
                            longitude=longitude,
                            location=location,
                            timestamp=timestamp)
            Earthquake(magnitude=magnitude)
            #db.create_all(), add & commit here?
            #Shall it be done in the server or here if it is here how can we do it withouth __main__

    #TODO: q2->How can we db.create_all(), add and commit here?
    #TODO: q3->How to get the latest earthquakes depending on location?Ex. Get all in CA region



############################### DRAFT OF HOW TO GET DATA FROM QUAKE FEEDS ########################################################
#QuakeFeed(user_value, "hour")
# feed = QuakeFeed(user.user_settings.user_value, "hour")
feed = QuakeFeed("4.5", "hour")


#This will get us the title depending on the earthquake event index
#idx will depend on the location
title = feed.event_title(0) #Ex. 'USGS Magnitude 4.5+ Earthquakes, Past Day'

#Get magnitude of the earthquake
magnitude = feed.magnitude(0)

#Get location coordinates
coordinates = feed.location(0)
latitude = coordinates[0]
longitude = coordinates[1]

#Get all location coordinates of all earthquakes in the last hour
feed.locations
list(feed.locations)

#This will give us the time in format
timestamp = feed.event_time(0) #Ex. datetime.datetime(2015, 4, 16, 19, 18, 39, tzinfo=datetime.timezone.utc)
