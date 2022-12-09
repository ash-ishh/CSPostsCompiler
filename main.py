from twitter import Twitter
from posts import fetch_open_ai_feed, fetch_deepmind_feed
from utils import get_checkpoint, set_checkpoint

import textwrap

CHECKPOINT = get_checkpoint()
TWITTER = Twitter()

def format_entry(entry):
    text = textwrap.dedent(f"""
    {entry['link']}
    {entry['summary']}
    """)
    if len(text) > 280:
        text = f"{text[:278]}.."
    return text

def process_open_ai():
    # TODO: Move same processing in genric function
    platform = 'openai'
    last_processed_date_string = CHECKPOINT.get(platform)
    print(f"{platform} - Last processed date for {platform}: {last_processed_date_string}")
    feed = fetch_open_ai_feed(last_processed_date_string)
    print(f"{platform} - Found {len(feed)} new blog posts")
    try:
        for entry in feed:
            tweet = format_entry(entry)
            print(f"{platform} - {tweet}")
            TWITTER.update_status(tweet)
            CHECKPOINT[platform] = entry['published']
    except Exception as e:
        print(e)
        set_checkpoint(CHECKPOINT) # if something goes wrong update checkpoint to avoid duplicate tweets
    if entry:
        set_checkpoint(CHECKPOINT)

def process_deepmind():
    # TODO: Move same processing in genric function
    platform = 'deepmind'
    last_processed_date_string = CHECKPOINT.get(platform)
    print(f"{platform} - Last processed date for {platform}: {last_processed_date_string}")
    feed = fetch_open_ai_feed(last_processed_date_string)
    print(f"{platform} - Found {len(feed)} new blog posts")
    try:
        for entry in feed:
            tweet = format_entry(entry)
            print(f"{platform} - {tweet}")
            TWITTER.update_status(tweet)
            CHECKPOINT[platform] = entry['published']
    except Exception as e:
        print(e)
        set_checkpoint(CHECKPOINT) # if something goes wrong update checkpoint to avoid duplicate tweets
    if entry:
        set_checkpoint(CHECKPOINT)


def main():
    process_open_ai()
    process_deepmind()

if __name__ == "__main__":
    main()