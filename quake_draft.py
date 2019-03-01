
############################### DRAFT OF HOW TO GET DATA FROM QUAKE FEEDS ########################################################

ALLOWED_LEVELS  = { "significant", "4.5", "2.5", "1.0", "all" }
ALLOWED_PERIODS = { "hour", "day", "week", "month" }
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

#sort eqs
sorted_quakes = sorted(user_quakes, key=lambda q: q['properties'].get('time', 0), reverse=True)
#Get time of the latest earthquake
latest_quake_time = list(feed)[0]['properties']['time'] #1551317554070
