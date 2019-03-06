from quakefeeds import QuakeFeed
import schedule
import time

from model import NaturalDisaster, Earthquake

ALLOWED_LEVELS  = { "significant", "4.5", "2.5", "1.0", "all" }
ALLOWED_PERIODS = { "hour", "day", "week", "month" }


def get_all_earthquakes(level, period):
    """Get all earthquakes denpending on magnitude and period we get a QuakeFeed object"""

    all_earthquakes = QuakeFeed(level, period)

    return all_earthquakes


def get_time_from_earthquake(feed, idx):
    """Get time from earthquake in miliseconds since the epoch"""

    time_ms = feed[idx]["properties"]["time"]

    return time_ms

def get_coords(feed, idx):
    """Get coordinates from earthquake in a tuple (lat, lng)"""

    coord = feed.location(idx)
    lng = coord[0]
    lat = coord[1]

    return (lat, lng)


def get_new_earthquake(level, period):
    """Get most recent earthquake object"""

    new_earthquake = None

    last_feed = get_all_earthquakes(level, period) #Quake feed object
    print("Last feed element zero is: ", last_feed[0])
    new_feed = get_all_earthquakes(level, period)

    #schedule get_all_earthquakes every 5 secs, compare results
    if last_feed:
        last_feed_time = get_time_from_earthquake(0, last_feed)
        new_feed_time = get_time_from_earthquake(0, new_feed)

        while last_feed_time == new_feed_time:
            new_feed = get_all_earthquakes(level, period)
            new_feed_time = get_time_from_earthquake(0, new_feed)
            # new_feed = ["New Earthquake info"] tests to make sure logic worked
            # print("New feed is now: ", new_feed)
            # print("Last feed is now: ", last_feed)

        #once new feed is different we will output new_earthquake
        new_earthquake_feed = new_feed
        print("New earthquake is: ", new_earthquake)
        print("New earthquake time: ", new_feed.event_time(0))

        save_quake_into_db(new_earthquake_feed)

        return new_earthquake_feed # type: QuakeFeed obj
        #TODO: refactor code to be able to grab multiple new earthquake []
        # then append to list all the new_earthquakes

def create_earthquake_for_db(feed, idx=0):
    """Save earthquake into database using feed methods to get data"""

    nat_type = "earthquake"
    title = feed.event_title(idx) #Ex. 'USGS Magnitude 4.5+ Earthquakes, Past Day'

    #Get magnitude of the earthquake
    magnitude = feed.magnitude(idx)

    #Get location coordinates
    coordinates = feed.location(idx)
    longitude = str(coordinates[0])
    latitude = str(coordinates[1])

    #Get place description
    location = feed.place(idx)

    #This will give us the time in format
    timestamp = feed.event_time(idx) #Ex. datetime.datetime(2015, 4, 16, 19, 18, 39, tzinfo=datetime.timezone.utc)


    earthquake = Earthquake(magnitude=magnitude)


    nat_disaster = NaturalDisaster(title=title,
                                   nat_type=nat_type,
                                   latitude=latitude,
                                   longitude=longitude,
                                   location=location,
                                   timestamp=timestamp)

    earthquake.natural_disaster = nat_disaster

    return earthquake



# def schedule_first_earthquake():
#     #do this only once
#     schedule.every(5).seconds.do(get_all_earthquakes, level="all", period="hour")

# if __name__ == '__main__':


    # schedule.every(5).seconds.do(get_new_earthquake, level="all", period="hour")
    #
    # # schedule.run_continuously(1)
    # #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
