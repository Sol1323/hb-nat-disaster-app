from quakefeeds import QuakeFeed
import schedule
import time

from model import User, Contact, Phone, Alert, NaturalDisaster, Earthquake, connect_to_db, db

from server import app


##############################  PSEUDOCODE  ################################################################
#Always getting in the past hour to get the most recent earthquakes
    #Define last_feed of QuakeFeed()
    #Define new_feed of QuakeFeed()

    #Compare new_feed time vs. last_feed time
        #If they are not equal
            #Redefine new_feed as last_feed
            #return last_earthquake on the new_feed

#magnitude will be what the user user inputs as setting
# get all settings with eq_magnitude
# get user_value for the magnitude
# pass magnitude into the QuakeFeed instance
#############################################################################################################

ALLOWED_LEVELS  = { "significant", "4.5", "2.5", "1.0", "all" }
ALLOWED_PERIODS = { "hour", "day", "week", "month" }


def get_all_earthquakes(level, period):
    """Get all earthquakes denpending on magnitude and period"""

    all_earthquakes = QuakeFeed(level, period)
    # schedule.every(5).seconds.do(get_all_earthquakes, level="all", period="hour")
    return all_earthquakes

# def schedule_first_earthquake():
#     #do this only once
#     schedule.every(5).seconds.do(get_all_earthquakes, level="all", period="hour")

def get_time_from_earthquake(idx, feed):
    """Get time from earthquake"""

    time = feed[idx]["properties"]["time"]

    return time




def get_new_earthquake(level, period):
    """Get most recent earthquake"""
    # now = datetime.datetime.now()
    new_earthquake = None
    # last_feed = None
    # new_feed = None
    # last_feed = get_all_earthquakes(level, period)
    #instantiante new request if it is the first time
    # if last_feed == None and new_feed == None:
    #     last_feed = get_all_earthquakes(level, period)
    #     return
    last_feed = get_all_earthquakes("all", "hour") #Quake feed object
    print("Last feed element zero is: ", last_feed[0])
    new_feed = get_all_earthquakes(level, period)

    #schedule get_all_earthquakes every 5 secs, compare results

    while last_feed[0] == new_feed[0]:
        new_feed = get_all_earthquakes(level, period)
        # new_feed = ["New Earthquake info"] test to make sure logic worked
        print("New feed is now: ", new_feed)
        #once new feed is different

    new_earthquake = new_feed[0]
    print(new_earthquake)

    return new_earthquake

    #
    # last_feed_time = get_time_from_earthquake(0, last_feed)
    # print(last_feed_time)
    # new_feed_time = get_time_from_earthquake(0, new_feed)
    # # new_feed_time = last_feed_time + 5000
    #
    # if last_feed_time != new_feed_time:
    #     #Get most recent earthquake is the first element in the feed
    #     new_feed = get_all_earthquakes(level, period)
    #     new_earthquake = new_feed[0]
    #     #redifine last_feed as the new_feed since they are different
    #     last_feed = new_feed

    # print(new_earthquake)
    # return schedule.CancelJob


# def get_all_earthquakes(level, period):
#     """Get all earthquakes denpending on magnitude string"""
#     #TODO: q1->We want to get the most recent earthquakes by the hour depending on the user's value?
#     feed = QuakeFeed(level, period)
#
#     if feed:
#         for idx in range(0, len(feed)):
#             title = feed.event_title(idx)
#             magnitude = feed.magnitude(idx)
#             timestamp = feed.event_time(idx)
#             location = feed.place(idx)
#
#             coordinates = feed.location(idx) #coord = []
#             latitude = coordinates[0]
#             longitude = coordinates[1]

            # NaturalDisaster(title=title,
            #                 latitude=latitude,
            #                 longitude=longitude,
            #                 location=location,
            #                 timestamp=timestamp)
            # Earthquake(magnitude=magnitude)
            #
            #TODO: db.create_all(), add & commit here in seed.py or when there is a match in server.py

    #TODO: q3->How to get the latest earthquakes depending on location?Ex. Get all in CA region

# last_feed = get_all_earthquakes("all", "hour")
#Need to create a timer that trigers the call every 30seconds for ex.

if __name__ == '__main__':
    # request = get_new_earthquake("all", "hour")
    schedule.every(5).seconds.do(get_new_earthquake, level="all", period="hour")

    # schedule.run_continuously(1)

    while True:
        schedule.run_pending()
        time.sleep(1)
