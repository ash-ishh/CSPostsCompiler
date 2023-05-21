import logging

import feedparser

from dateutil.parser import parse

from bs4 import BeautifulSoup

from utils import get_checkpoint, set_checkpoint
from twitter import Twitter

logger = logging.getLogger(__name__)


class FeedParser:
    def __init__(self, url, max=1):
        self.url = url
        self.max = max

    def fetch(self, last_processed_date=None):
        feed = feedparser.parse(self.url)
        if last_processed_date:
            entries = [entry for entry in feed.entries if parse(
                entry.published) > last_processed_date]
            logger.info(f"Fetched {len(entries)} for {self.url} "
                        f"from {last_processed_date}")
        else:
            # get only max latest entry when last processed date is not
            # provided
            entries = feed.entries[:self.max]
            logger.info(f"Fetched {len(entries)} for {self.url}")
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
            'netflix': 'https://netflixtechblog.com/feed',
            'aws-architecture': 'https://aws.amazon.com/blogs/architecture/feed/',
            'zerodha': 'https://zerodha.tech/index.xml'
        }
        self.rss_feed_url = self.rss_feed_url_mapping[self.name]

    def set_trimmed_feed(self):
        logger.info("Setting: trimmed_feed")
        for entry in self.feed:
            trimmed_entry = {}
            trimmed_entry['title'] = entry.title
            try:
                summary_soup = BeautifulSoup(entry.summary, 'html.parser')
                if summary_soup.find():
                    summary_ps = summary_soup.find_all('p')
                    summary = '\n'.join([summary_p.get_text()
                                        for summary_p in summary_ps])
                else:
                    summary = entry.summary
            except AttributeError:
                logger.error("summary missing from feed - setting as empty string")
                summary = ""
            trimmed_entry['summary'] = summary
            trimmed_entry['link'] = entry.link
            trimmed_entry['published'] = entry.published
            self.trimmed_feed.append(trimmed_entry)

    def normalize_feed(self):
        # TODO: Check if it can be taken out
        # TODO: Caution they can be dynamic
        # Available fields
        _ = {
            'openai': ['title', 'title_detail', 'summary', 'summary_detail',
                       'links', 'link', 'id', 'guidislink', 'tags', 'published',
                       'published_parsed'],
            'deepmind': ['title', 'title_detail', 'summary', 'summary_detail',
                         'links', 'link', 'id', 'guidislink', 'published',
                         'published_parsed', 'media_content',
                         'media_thumbnail', 'href'],
            'netflix': ['title', 'title_detail', 'links', 'link', 'id',
                        'guidislink', 'tags', 'authors', 'author',
                        'author_detail', 'published', 'published_parsed',
                        'updated', 'updated_parsed', 'content', 'summary'],
            'aws-architecture': ['title', 'title_detail', 'links', 'link',
                                 'authors', 'author', 'author_detail',
                                 'published', 'published_parsed', 'tags',
                                 'id', 'guidislink', 'summary',
                                 'summary_detail', 'content'],
            'zerodha': ['title', 'title_detail', 'links', 'link', 'published',
                        'published_parsed', 'id', 'guidislink', 'summary',
                        'summary_detail']
        }
        # Required fields
        _ = ['title', 'summary', 'link', 'published']

    def fetch_and_set_trimmed_feed(self, last_processed_date_string):
        url = self.rss_feed_url
        logger.info(f"Processing: {url}")
        if self.last_processed_date_string:
            self.last_processed_date = parse(last_processed_date_string)
        logger.info(f"Last processed_date: {self.last_processed_date}")
        feed_parser_instance = FeedParser(url)
        self.feed = feed_parser_instance.fetch(self.last_processed_date)
        self.normalize_feed()
        try:
            self.set_trimmed_feed()
        except AttributeError:
            logger.exception(f"Check below stack trace for {url} some attribute is missing")

    def format_entry(self, entry):
        link = entry['link'].strip()
        # summary
        _ = entry['summary'].strip()
        """
        #TODO: Improve summary
        summary = re.sub(r'\n+', '\n',summary)
        available_chars = 280 - 2 - len(link)
        #TODO: Check twitter link char count
        if len(summary) > available_chars:
            summary = f'"{summary[:available_chars-5]}.."'
        else:
            summary = f'"{summary}"'
        text = f"{summary}\n{link}"
        print(f"Final tweet size: {len(text)}")
        """
        text = link
        return text

    def process(self):
        logger.info(f"Processing {self.name}")
        if not self.checkpoint and not self.last_processed_date_string:
            # if checkpoint is not set while creating instance
            # or if last_processed_date_string is not set
            logger.info("Fetching: checkpoint")
            logger.info(f"Before fetch: checkpoint - {self.checkpoint}, "
                        "last_processed_date_string - "
                        f"{self.last_processed_date_string}")
            self.checkpoint = get_checkpoint()
        if not self.last_processed_date_string:
            # if last_processed_date_string is directly given no need to get
            # it from checkpoint
            logger.info("Setting: last_process_date_string")
            self.last_processed_date_string = self.checkpoint.get(self.name)
        logger.info(f"Last processed date - {self.last_processed_date_string}")
        self.fetch_and_set_trimmed_feed(self.last_processed_date_string)
        logger.info(
            f"For {self.name} - found {len(self.trimmed_feed)} new blog posts")
        try:
            for entry in self.trimmed_feed:
                tweet = self.format_entry(entry)
                logger.info(f"Sending to twitter: - {tweet}")
                self.twitter.update_status(tweet)
                if self.checkpoint:
                    self.checkpoint[self.name] = entry['published']
        except Exception:
            logger.exception("Issue in tweeting")
            if self.checkpoint:
                logger.info("Setting checkpoint in case of exception")
                # if something goes wrong update checkpoint to avoid duplicate
                # tweets
                set_checkpoint(self.checkpoint)
        if self.trimmed_feed and self.checkpoint:
            # if feed then only set checkpoint
            logger.info("Setting checkpoint")
            set_checkpoint(self.checkpoint)
