#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os.path
import re

import arrow
from bs4 import BeautifulSoup
from jinja2 import Template
import requests
from xml.sax.saxutils import escape

import config  # TODO

_logger = logging.getLogger(__name__)


def clean_timestamp(timestamp):
    return arrow.Arrow.fromtimestamp(float(timestamp))


class Tweet(object):
    PICTURE_REGEX = re.compile('pic\.twitter\.')
    TWEET_DELETE = (
        ' class="js-tweet-text tweet-text"',
        ' class="twitter-atreply pretty-link"',
        ' class="invisible"',
        ' class="js-display-url"',
        ' class="twitter-hashtag pretty-link js-nav"',
        ' class="twitter-timeline-link"',
        ' class="tco-ellipsis"',
        ' class="invisible"',
        ' class="ProfileTweet-text js-tweet-text u-dir"',
        ' data-query-source="hashtag_click"',
        ' rel="nofollow"',
        ' target="_blank"',
        ' data-expanded-url=".*?"',
        ' title=".*?"',
        ' data-query-source="hashtag_click"',
        ' dir="ltr"',
        '<span><span>&nbsp;</span>.*</span>',
        '<span>http://</span>',
        ' data-pre-embedded="true"',
        '<p>', '</p>',
        '<span>', '</span>',
        '<strong>', '</strong>',
    )
    TWEET_REPLACE = {
        '<s>@</s>': '@',
        'href="/': 'href="http://twitter.com/',
    }

    def __init__(self, text, meta, pictures=False):
        self.raw_text = str(text).decode('UTF-8')
        self.text = text

        self.link = None
        self.date = None
        self.author = None

        self.set_info(meta)
        self.pictures = pictures

    def __repr__(self):
        return '<Tweet "{text}" at {date}'.format(text=self.__str__(), date=self.date)

    def __str__(self):
        return self.clean_text()

    def set_info(self, meta):
        href = meta.find_all('a')[-1]
        self.link = re.sub(r'\(u\'href\', u\'(.*)\'\)', r'\1', str(href.attrs['href']))

        span = meta.find('span', 'js-short-timestamp')
        timestamp = re.sub(r'\(u\'data-time\', u\'(.*)\'\)', r'\1', str(span.attrs['data-time']))

        self.date = clean_timestamp(timestamp)
        self.author = self.link.split('/')[1]

    def clean_text(self):
        output = self.raw_text
        for old, new in [(item, '') for item in self.TWEET_DELETE] + self.TWEET_REPLACE.items():
            output = re.sub(old, new, output)

        return output

    def get_pic(self):
        pic = None
        if 'pic.twitter.com' in self.raw_text:
            pic_url = 'http://' + self.text.find('a', text=self.PICTURE_REGEX).text

            content = requests.get(pic_url)
            soup = BeautifulSoup(content.text)
            pic = re.findall(r'(https?://pbs.twimg.com/media/\S+\.\S+:large)', str(soup))[0]
        return pic

    def to_jinja2(self):
        template = {
            'title': escape(self.text.text),
            'author': self.author,
            'link':  self.link,
            'date': self.date.strftime('%a, %d %b %Y %H:%M:%S %z'),
            'content': self.clean_text()
        }
        if self.pictures and self.get_pic():
            template.update({'pic': self.get_pic()})
        return template


class TweetGetter(object):
    directory = None  # to be defined

    def __init__(self, url, obj):
        self.url = url
        self.obj = obj

        self.title = None
        self.tweets = None

        self.parse_twitter()

    def parse_twitter(self):
        content = requests.get(self.url.format(self.obj))
        if content.status_code == 404:
            _logger.warning('Error 404: Account not found')
            return

        _logger.debug('Connection successful!')
        soup = BeautifulSoup(content.text)

        self.title = soup.title.string
        self.tweets = []

        get_meta_text = lambda c: zip(
            c.find_all(["small", "div"], {"class": ["time", "ProfileTweet-authorDetails"]}),
            c.find_all("p", "js-tweet-text")
        )

        for content in soup.find_all("div", {'class': ["content", "StreamItem"]}):
            for meta, text in get_meta_text(content):
                self.tweets.append(Tweet(text, meta))

    def to_rss(self, server="."):
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'rss-model.tpl')
        with open(template_path) as template_file:
            items = list(map(lambda tweet: tweet.to_jinja2(), self.tweets))
            template = Template(template_file.read())
            return template.render(
                server=server, directory=self.directory, descriptor=self.obj,
                title=self.title, url=self.url.format(self.obj), tweets=items
            )


class UserTweetGetter(TweetGetter):
    def __init__(self, username):
        self.directory = 'user'
        super(UserTweetGetter, self).__init__("https://twitter.com/{0}/with_replies", username)


class HashtagTweetGetter(TweetGetter):
    def __init__(self, hashtag):
        self.directory = 'htag'
        super(HashtagTweetGetter, self).__init__("https://twitter.com/search?q=%23{0}", hashtag)


class FeedManager(object):
    HANDLERS = {
        'user': UserTweetGetter,
        'htag': HashtagTweetGetter,
    }

    @staticmethod
    def create_file_if_needed(file_path):
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if not os.path.exists(file_path):
            with open(file_path, 'a'):
                pass

        return file_path

    def update_file_path(self, kind):
        return self.create_file_if_needed(os.path.join(config.XML_DIR, kind, '{}.txt'.format(kind)))

    def cached_file_path(self, kind, feed):
        return self.create_file_if_needed(os.path.join(config.XML_DIR, kind, '{}.xml'.format(feed)))

    def add_feed_to_update_set(self, kind, feed):
        with open(self.update_file_path(kind), "w+") as file_io:
            all_feeds = set(line.strip() for line in file_io.readlines())
            all_feeds.add(feed)
            file_io.seek(0)
            file_io.write("\n".join(all_feeds))

    def feed_update_set(self, kind):
        with open(self.update_file_path(kind)) as file_in:
            return set(line.strip() for line in file_in.readlines())

    def get(self, kind, feed):
        if kind not in self.HANDLERS:
            raise NotImplementedError("No Twitter handlers for {} kind".format(kind))
        cached = self.get_cached(kind, feed)
        if cached:
            return cached

        tweets = self.HANDLERS[kind](feed)
        self.add_feed_to_update_set(kind, feed)
        return self.add_to_cache(kind, feed, tweets)

    def add_to_cache(self, kind, feed, tweets):
        _logger.info("Update rss cache for {}/{}".format(kind, feed))
        data = tweets.to_rss().encode('utf-8')
        with open(self.cached_file_path(kind, feed), "w") as file_out:
            file_out.write(data)
        return data

    def get_cached(self, kind, feed):
        cache_path = self.cached_file_path(kind, feed)
        is_valid = lambda path: arrow.utcnow() < arrow.get(os.path.getmtime(path)).replace(minutes=+config.CACHE)
        if not os.path.isfile(cache_path) or not is_valid(cache_path):
            _logger.info("Need to update cache for feed {}/{}".format(kind, feed))
            return None

        _logger.info("Get cached version for feed {}/{}".format(kind, feed))
        with open(cache_path) as cache:
            return cache.read()

    def update_all_feeds(self):
        for kind in self.HANDLERS:
            for obj in self.feed_update_set(kind):
                _logger.info("Update {}/{} feed".format(kind, obj))
                self.get(kind, obj)
