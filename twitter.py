import os
import tweepy

from dotenv import load_dotenv
load_dotenv()
# Global def so that it does not create new client for each platform
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
TESTING_MODE = os.getenv("TESTING_MODE")
client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

class Twitter:
    def __init__(self):
        self.client = client

    def update_status(self, tweet):
        if TESTING_MODE.lower() == 'false':
            self.client.create_tweet(text=tweet)
        else:
            print(f"Testing mode on: {tweet}")