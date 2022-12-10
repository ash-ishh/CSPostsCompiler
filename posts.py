import feedparser
import re

from dateutil.parser import parse
from bs4 import BeautifulSoup
from utils import get_checkpoint, set_checkpoint

from twitter import Twitter


class FeedParser:
    def __init__(self, url, max=1):
        self.url = url
        self.max = max
    
    def fetch(self, last_processed_date):
        feed = feedparser.parse(self.url)
        if last_processed_date:
            entries = [entry for entry in feed.entries if parse(entry.published) > last_processed_date]
        else:
            entries = feed.entries[:self.max] # get only max latest entry when last processed date is not provided
        return entries

class Platform:
    def __init__(self, name, checkpoint=None, last_processed_date_string=None):
        self.name = name
        self.twitter = Twitter()
        self.checkpoint = checkpoint
        self.last_processed_date_string = last_processed_date_string
        self.last_processed_date = None
        self.feed = list()
        self.trimmed_feed = list()
        self.rss_feed_url_mapping = {
            'openai': 'https://openai.com/blog/rss/',
            'deepmind': 'https://www.deepmind.com/blog/rss.xml',
            'netflix': 'https://netflixtechblog.com/feed'
        }

    def set_trimmed_feed(self):
        print("Setting: trimmed feed")
        for entry in self.feed:
            trimmed_entry = {}
            trimmed_entry['title'] = entry.title
            summary_soup = BeautifulSoup(entry.summary, 'html.parser')
            summary = summary_soup.get_text()
            trimmed_entry['summary'] = summary
            trimmed_entry['link'] = entry.link
            trimmed_entry['published'] = entry.published
            self.trimmed_feed.append(trimmed_entry)
    
    def normalize_feed(self):
        #TODO: Check if it can be taken out
        available_fields = {
            'openai': ['title', 'title_detail', 'summary', 'summary_detail', 'links', 'link', 'id', \
                       'guidislink', 'tags', 'authors', 'author', 'author_detail', 'published', \
                       'published_parsed', 'media_content', 'content'],
            'deepmind': ['title', 'title_detail', 'summary', 'summary_detail', 'links', 'link', 'id', \
                         'guidislink', 'published', 'published_parsed', 'media_content', 'media_thumbnail', 'href'],
            'netflix': ['title', 'title_detail', 'links', 'link', 'id', 'guidislink', 'tags', 'authors', 'author', \
                        'author_detail', 'published', 'published_parsed', 'updated', 'updated_parsed', 'content', 'summary']
        }
        required_fields = ['title', 'summary', 'link', 'published']
 
    def fetch_and_set_trimmed_feed(self, last_processed_date_string):
        url = self.rss_feed_url_mapping[self.name]
        print(f"Processing: {url}")
        if self.last_processed_date_string:
            self.last_processed_date = parse(last_processed_date_string)
        print(f"Last processed_date: {self.last_processed_date}")
        feed_parser_instance = FeedParser(url)
        self.feed = feed_parser_instance.fetch(self.last_processed_date)
        self.normalize_feed()
        self.set_trimmed_feed()
 
    def format_entry(self, entry):
        link = entry['link'].strip()
        summary = entry['summary'].strip().capitalize()
        summary = re.sub(r'\n+', '\n',summary)
        available_chars = 280 - len(link)
        #TODO: Check twitter link char count
        if len(summary) > available_chars:
            summary = f"{summary[:available_chars-3]}.."
        text = f"{summary}\n{link}"
        print(f"Final tweet size: {len(text)}")
        return text

    def process(self):
        print(f"Processing {self.name}")
        if not self.checkpoint and not self.last_processed_date_string:
            # if checkpoint is not set while creating instance
            # or if last_processed_date_string is not set
            print("Fetching: checkpoint")
            print(f"Before fetch: checkpoint - {self.checkpoint}, last_processed_date_string - {self.last_processed_date_string}")
            self.checkpoint = get_checkpoint()
        if not self.last_processed_date_string:
            # if last_processed_date_string is directly given no need to get it from checkpoint
            print("Setting: last_process_date_string")
            self.last_processed_date_string = self.checkpoint.get(self.name)
        print(f"Info: Last processed date - {self.last_processed_date_string}")
        self.fetch_and_set_trimmed_feed(self.last_processed_date_string)
        print(f"{self.name} - Found {len(self.trimmed_feed)} new blog posts")
        try:
            for entry in self.trimmed_feed:
                tweet = self.format_entry(entry)
                print(f"Sending to twitter: - {tweet}")
                self.twitter.update_status(tweet)
                if self.checkpoint:
                    self.checkpoint[self.name] = entry['published']
        except Exception as e:
            print(e)
            if self.checkpoint:
                print("Setting checkpoint in case of exception")
                set_checkpoint(self.checkpoint) # if something goes wrong update checkpoint to avoid duplicate tweets
        if self.trimmed_feed and self.checkpoint:
            # if feed then only set checkpoint
            print("Setting checkpoint")
            set_checkpoint(self.checkpoint)