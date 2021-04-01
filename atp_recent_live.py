"""
Script that queries @atpfm's twitter feed for a recent tweet (within 30
minutes) stating when their show will be live. The script exits with status 0
if such a tweet exists, exits with status 1 otherwise

Author: Stephen Kim
Date: March 31st, 2021
"""
from datetime import datetime, timedelta
from dotenv import dotenv_values
import twitter
import pytz
import time
import re

# returns a dict of variables in .env file
config = dotenv_values()
api = twitter.Api(consumer_key=config['TWITTER_CONSUMER_KEY'],
                  consumer_secret=config['TWITTER_CONSUMER_SECRET'],
                  access_token_key=config['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=config['TWITTER_ACCESS_TOKEN_SECRET'])

def main():
    tweets = api.GetUserTimeline( \
        screen_name='atpfm', \
        exclude_replies=True, \
        include_rts=False, \
        count=10,
        )
    # regex pattern for matching tweet
    p = re.compile('live in .* minutes')
    for status in tweets:
        tweet = status.text
        # find first tweet matching pattern "live in x minutes"
        if (p.search(tweet) is not None):

            # grab start time, localize
            d = datetime.strptime(status.created_at, "%a %b %d %H:%M:%S %z %Y")
            d = d.astimezone(tz=pytz.timezone('US/Eastern'))
            now = datetime.now()

            # from https://stackoverflow.com/questions/2788871/date-difference-in-minutes-in-python
            # Convert to Unix timestamp, in seconds
            d1_ts = time.mktime(d.timetuple())
            d2_ts = time.mktime(now.timetuple())

            # They are now in seconds, subtract and then divide by 60 to get minutes.
            length = int(d2_ts-d1_ts) / 60
            status = 0 if length < 30 else 1
            print("%r minutes ago: %r" % (str(length), tweet))
            exit(status)

if __name__ == "__main__":
    main()
