from twitter import Twitter
from posts import fetch_open_ai_feed, fetch_deepmind_feed
from utils import get_checkpoint, set_checkpoint
from main import main

def test_update_status():
    text = "Hello World!"
    twitter = Twitter()
    twitter.update_status(text)

def test_checkpoint_object():
    checkpoint = get_checkpoint()
    checkpoint['openai']= 'Thu, 03 Nov 2022 17:00:02 GMT'
    set_checkpoint(checkpoint)

def test_open_ai_feed():
    last_processed_date = 'Thu, 03 Nov 2022 17:00:02 GMT'
    feed = fetch_open_ai_feed(last_processed_date)
    for entry in feed:
        print(entry)

def test_deepmind_feed():
    last_processed_date = 'Thu, 07 Dec 2022 17:00:02 GMT'
    feed = fetch_deepmind_feed(last_processed_date)
    for entry in feed:
        print(entry)

def test_main():
    main()

# test_update_status()
# test_checkpoint_object()
# test_open_ai_feed()
# test_deepmind_feed()
# test_main()
