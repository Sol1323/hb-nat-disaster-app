from quakefeeds import QuakeFeed
import schedule
import time

# from model import User, Contact, Phone, Alert, NaturalDisaster, Earthquake, connect_to_db, db



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
    """Get all earthquakes denpending on magnitude and period we get a QuakeFeed object"""

    all_earthquakes = QuakeFeed(level, period)
    # schedule.every(5).seconds.do(get_all_earthquakes, level="all", period="hour")
    return all_earthquakes

# def schedule_first_earthquake():
#     #do this only once
#     schedule.every(5).seconds.do(get_all_earthquakes, level="all", period="hour")

def get_time_from_earthquake(idx, feed):
    """Get time from earthquake in miliseconds milliseconds since the epoch"""

    time_ms = feed[idx]["properties"]["time"]

    return time_ms


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

        while last_feed.event(0) == new_feed.event(0):
            new_feed = get_all_earthquakes(level, period)
            new_feed_time = get_time_from_earthquake(0, new_feed)
            # new_feed = ["New Earthquake info"] tests to make sure logic worked
            # print("New feed is now: ", new_feed)
            # print("Last feed is now: ", last_feed)

        #once new feed is different we will output new_earthquake
        new_earthquake = new_feed
        print("New earthquake is: ", new_earthquake)
        print("New earthquake time: ", new_feed.event_time(0))

        return new_earthquake
        #We will return the whole QuakeFeed object to be able to grab data with feed individual methods
        #Remember to use idx 0 to grab the new_earthquake in the feed and save it in the database
        #TODO: refactor code to be able to grab multiple new earthquake []
        # then append to list all the new_earthquakes



if __name__ == '__main__':
    # request = get_new_earthquake("all", "hour")
    schedule.every(5).seconds.do(get_new_earthquake, level="all", period="hour")

    # schedule.run_continuously(1)
    #
    while True:
        schedule.run_pending()
        time.sleep(1)
