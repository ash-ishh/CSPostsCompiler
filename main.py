from twitter import Twitter
from posts import fetch_open_ai_feed
from utils import get_checkpoint, set_checkpoint

import textwrap

CHECKPOINT = get_checkpoint()
TWITTER = Twitter()

def format_entry(entry):
    text = textwrap.dedent(f"""
    {entry['title']}
    {entry['link']}
    """)
    return text

def process_open_ai():
    platform = 'openai'
    last_processed_date_string = CHECKPOINT[platform]
    print(f"{platform} - Last processed date for OpenAI: {last_processed_date_string}")
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

if __name__ == "__main__":
    main()