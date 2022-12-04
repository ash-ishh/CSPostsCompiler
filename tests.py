from twitter import Twitter
from posts import fetch_open_ai_feed
from utils import get_checkpoint, set_checkpoint
from main import main

def test_update_status():
    text = "Hello World!"
    twitter = Twitter()
    twitter.update_status(text)

def test_open_ai_feed():
    feed = fetch_open_ai_post()
    for entry in feed:
        print(entry)

def test_checkpoint_object():
    checkpoint = get_checkpoint()
    checkpoint['openai']= 'Thu, 03 Nov 2022 17:00:02 GMT'
    set_checkpoint(checkpoint)

def test_main():
    main()

# test_update_status()
# test_open_ai_feed()
# test_checkpoint_object()
# test_main()
