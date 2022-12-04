import os
import tweepy

from dotenv import load_dotenv
load_dotenv()

class Twitter:
    def __init__(self):
        CONSUMER_KEY = os.getenv("CONSUMER_KEY")
        CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
        self.client = tweepy.Client(consumer_key=CONSUMER_KEY,
                                    consumer_secret=CONSUMER_SECRET,
                                    access_token=ACCESS_TOKEN,
                                    access_token_secret=ACCESS_TOKEN_SECRET)

    def update_status(self, tweet):
        self.client.create_tweet(text=tweet)