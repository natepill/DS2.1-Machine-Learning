from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import requests
import tweepy
import env #Custom env file for tweepy keys
import dataset
import json
import os


'''
Open a persistent connection to the Twitter API.
Process each tweet that we receive.
Store the processed tweets.

we’ll need to use a programming paradigm called event-driven programming

'''



# NOTE: CHANGE THE TERMS IN THE ARRAY TO WHAT TERMS OF TWEETS YOU WANT TO SCRAPE
TRACK_TERMS = ["trump", "clinton", "hillary clinton", "donald trump"]



db = dataset.connect("sqlite:///tweets.db")
table = db["tweets"]



# Twitter sent, and call an appropriate method to deal with the specific data type. It's possible to deal with events like users sending direct messages, tweets being deleted, and more. For now, we only care about when users post tweets. Thus, we'll need to override the on_status method:

#Overriding Tweepy's StreamListener class
class StreamListener(tweepy.StreamListener):
    '''Create a listener that prints the text of any tweet that comes from the Twitter API.'''

    def on_status(self, status):

        # If tweet is a retweet, then don’t process the tweet.
        if hasattr(status, 'retweeted_status'):
            return
        print(status.text)

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color

        #TODO: We could preprocess the tweets here by feeding each tweet as we stream them through our ML model
        # and then we can store the sentiment score along with these other features

        # Going to replace w/ Text Vectorization
        # Have to feed each tweet through ML model, then store that


        if coords is not None:
            coords = json.dumps(coords)
        # Other Tweet Properties: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
        # Cool Doc examples:
            # includeretweet_count — the number of times a tweet has been retweeted.
            # withheld_in_countries — the tweet has been withheld in certain countries.
            # favorite_count — the number of times the tweet has been favorited by other users.

        # From Docs
        # The user's description (status.user.description). This is the description the user who created the tweet wrote in their biography.
        #     The user's location (status.user.location). This is the location the user who created the tweet wrote in their biography.
        #     The screen name of the user (status.user.screen_name).
        #     When the user's account was created (status.user.created_at).
        #     How many followers the user has (status.user.followers_count).
        #     The background color the user has chosen for their profile (status.user.profile_background_color).
        #     The text of the tweet (status.text).
        #     The unique id that Twitter assigned to the tweet (status.id_str).
        #     When the tweet was sent (status.created_at).
        #     How many times the tweet has been retweeted (status.retweet_count).
        #     The tweet's coordinates (status.coordinates). The geographic coordinates from where the tweet was sent.


        # Storing tweets into an SQLlite db so they can be easily queried, or dumped out to csv for further analysis.
        table.insert(dict(
            user_description=description,
            user_location=loc,
            coordinates=coords,
            text=text,
            user_name=name,
            user_created=user_created,
            user_followers=followers,
            id_str=id_str,
            created=created,
            retweet_count=retweets,
            user_bg_color=bg_color
        ))
    # Override the on_error method of StreamListener so that we can handle errors coming from the Twitter API properly
    # The Twitter API will send a 420 status code if we're being rate limited. If this happens --> disconnect, any other error, keep going
    def on_error(self, status_code):
        if status_code == 420:
            return False



auth = tweepy.OAuthHandler(env.TWITTER_APP_KEY, env.TWITTER_APP_SECRET)
auth.set_access_token(env.TWITTER_KEY, env.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
# We pass in our stream_listener so that our callback functions are called
# stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
# stream.filter(track=TRACK_TERMS) # Start streaming tweets


print(db.tables)
print(db['tweets'].columns)
print(len(db['tweets']))
all_tweets = db['tweets'].all()
print(all_tweets)

for tweet in db['tweets']:
   print(tweet["text"])
