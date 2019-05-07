import tweepy
import dataset
from datafreeze import freeze
import json


db = dataset.connect("sqlite:///tweets.db")

result = db["tweets"].all()
# We’re now able to write each of our processed tweets to a database.
# Once they’re in a database, they can be easily queried, or dumped out to csv for further analysis.
freeze(result, format='csv', filename="all-tweets")
