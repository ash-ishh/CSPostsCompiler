from twitter import Twitter
from posts import Platform, FeedParser
from utils import get_checkpoint, set_checkpoint
from main import main

def test_update_status():
    text = "Hello World!"
    twitter = Twitter()
    twitter.update_status(text)

def test_get_checkpoint():
    checkpoint = get_checkpoint()
    print(checkpoint)


def test_update_checkpoint():
    checkpoint = {
        "openai": "Thu, 09 Dec 2022 17:00:02 GMT",
        "deepmind": "Thu, 09 Dec 2022 17:00:02 GMT"
    }
    set_checkpoint(checkpoint)


def test_open_ai_feed():
    platform_name = "openai"
    last_processed_date = "Thu, 07 Nov 2022 17:00:02 GMT"
    openai = Platform(platform_name, last_processed_date_string=last_processed_date) 
    openai.process()


def test_deepmind_feed():
    platform_name = "deepmind"
    last_processed_date = "Thu, 30 Nov 2022 17:00:02 GMT"
    deepmind = Platform(platform_name, last_processed_date_string=last_processed_date)
    deepmind.process()

def test_netflix_feed():
    platform_name = "netflix"
    netflix = Platform(platform_name)
    netflix.process()

def test_aws_archtecture_feed():
    platform_name = "aws-architecture"
    aws_architecture = Platform(platform_name)
    aws_architecture.process()

def test_zerodha_feed():
    platform_name = "zerodha"
    zerodha = Platform(platform_name)
    zerodha.process()

def test_feed_headers():
    platform_name = "zerodha"
    platform = Platform(platform_name)
    feed_parser_instance = FeedParser(platform.rss_feed_url)
    feed = feed_parser_instance.fetch()
    if feed:
        headers = list(feed[0].keys())
        print(headers)
    else:
        print("feed not found")

def test_main():
    main()

# test_update_status()
# test_checkpoint_object()
# test_update_checkpoint()
# test_get_checkpoint()
test_open_ai_feed()
# test_deepmind_feed()
# test_netflix_feed()
# test_zerodha_feed()
# test_feed_headers()
# test_main()