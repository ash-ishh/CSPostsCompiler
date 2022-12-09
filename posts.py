import feedparser
from dateutil.parser import parse

from bs4 import BeautifulSoup
from utils import get_checkpoint

class FeedParser:
    def __init__(self, url, max=1):
        self.url = url
        self.max = max
    
    def fetch(self, last_processed_date):
        feed = feedparser.parse(self.url)
        if last_processed_date:
            entries = [entry for entry in feed.entries if parse(entry.published) > last_processed_date]
        else:
            entries = feed.entries[:1] # get only latest entry where last processed date is not provided
        return entries

def create_trimmed_entries(feed):
    trimmed_feed = []
    for entry in feed:
        trimmed_entry = {}
        trimmed_entry['title'] = entry.title
        summary_soup = BeautifulSoup(entry.summary, 'html.parser')
        summary = summary_soup.get_text()
        trimmed_entry['summary'] = summary
        trimmed_entry['link'] = entry.link
        trimmed_entry['published'] = entry.published
        trimmed_feed.append(trimmed_entry)
    return trimmed_feed

def fetch_open_ai_feed(last_processed_date_string=None):
    url = "https://openai.com/blog/rss/"
    last_processed_date = parse(last_processed_date_string)
    open_ai_feed = FeedParser(url)
    feed = open_ai_feed.fetch(last_processed_date)
    # ['title', 'title_detail', 'summary', 'summary_detail', 'links', 'link', 'id', \
    # 'guidislink', 'tags', 'authors', 'author', 'author_detail', 'published', \
    # 'published_parsed', 'media_content', 'content']
    trimmed_feed = create_trimmed_entries(feed)
    return trimmed_feed

def fetch_deepmind_feed(last_processed_date_string=None):
    url = "https://www.deepmind.com/blog/rss.xml"
    last_processed_date = parse(last_processed_date_string)
    deep_mind_feed = FeedParser(url)
    feed = deep_mind_feed.fetch(last_processed_date)
    # ['title', 'title_detail', 'summary', 'summary_detail', 'links', 'link', 'id', \
    # 'guidislink', 'published', 'published_parsed', 'media_content', 'media_thumbnail', 'href'])
    trimmed_feed = create_trimmed_entries(feed)
    return trimmed_feed