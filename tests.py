from twitter import Twitter
from posts import Platform
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
        "openai": "Thu, 08 Dec 2022 17:00:02 GMT",
        "deepmind": "Thu, 07 Dec 2022 17:00:02 GMT"
    }
    set_checkpoint(checkpoint)

def test_open_ai_feed():
    paltform_name = 'openai'
    last_processed_date = 'Thu, 03 Sep 2022 17:00:02 GMT'
    openai = Platform(paltform_name, last_processed_date_string=last_processed_date)
    openai.process()


def test_deepmind_feed():
    paltform_name = 'deepmind'
    last_processed_date = 'Thu, 07 Sep 2022 17:00:02 GMT'
    deepmind = Platform(paltform_name, last_processed_date_string=last_processed_date)
    deepmind.process()

def test_netflix_feed():
    paltform_name = 'netflix'
    netflix = Platform(paltform_name)
    netflix.process()

def test_main():
    main()

# test_update_status()
# test_checkpoint_object()
# test_update_checkpoint()
# test_get_checkpoint()
# test_open_ai_feed()
# test_deepmind_feed()
test_netflix_feed()
# test_main()
