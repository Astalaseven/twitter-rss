#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import requests
import re
import arrow
import config
from jinja2 import Template

class Tweet(object):

    def __init__(self, text, meta, get_pics=False):
        self.raw_text = str(text).decode('UTF-8')
        self.set_info(meta)
        self.get_pics = get_pics

    def set_info(self, meta):
        for href in meta.findAll('a'):
            self.link = re.sub(r'\(u\'href\', u\'(.*)\'\)', r'\1', str(href.attrs[0]))

            span = meta.find('span')
            timestamp = re.sub(r'\(u\'data-time\', u\'(.*)\'\)', r'\1', str(span.attrs[1]))

            self.date = self.clean_timestamp(timestamp)
            self.author = self.link.split('/')[1]

    def __repr__(self):
        return '<Tweet "{text}"" at {date}'.format(text=self.__str__(), date=self.date)

    def __str__(self):
        return self.clean_text(True)

    def clean_text(self):
        output = self.raw_text

        to_delete = self.TWIT_DELETE
        to_replace = [{'<s>@</s>': '@'},
                      {'href="/': 'href="http://twitter.com/'}]
        for item in to_delete:
            output = re.sub(item, '', output)
        for item in to_replace:
            for old, new in item.items():
                output = re.sub(old, new, output)

        title = output
        to_delete = self.TWEET_DELETE
        for item in to_delete:
            title = re.sub(item, '', title)

        return [output, title]

    def get_pic(self):
        pic = None
        if 'pic.twitter.com' in self.raw_text:
            pic_url = 'http://' + str(re.sub(r'.*dir="ltr">pic.twitter.com/(.*?)</a>.*', r'pic.twitter.com/\1', self.raw_text.encode('utf8')))

            content = requests.get(pic_url)
            soup = BeautifulSoup(content.text)
            pic = re.findall(r'(https?://pbs.twimg.com/media/\S+\.\S+:large)', str(soup))[0]
        return pic

    def clean_timestamp(self,timestamp):
        return arrow.Arrow.fromtimestamp(float(timestamp))

    def to_jinja2(self):
        template = {
                'title' : self.clean_text()[1],
                'author'  : self.author,
                'link' : self.link,
                'date' : self.date.strftime('%a, %d %b %Y %H:%M:%S %z'),
                'content' : self.clean_text()[0]
            }
        if config.PICS is True and self.get_pic() != None:
            template.update({'pic' : self.get_pic()})
        return template

    TWIT_DELETE = [
        ' class="js-tweet-text tweet-text"',
        ' class="twitter-atreply pretty-link"',
        ' class="invisible"',
        ' class="js-display-url"',
        ' class="twitter-hashtag pretty-link js-nav"',
        ' class="twitter-timeline-link"',
        ' class="tco-ellipsis"',
        ' class="invisible"',
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
        '<p>', '</p>', '<span>', '</span>', '<strong>', '</strong>']

    TWEET_DELETE = [
        '<p>', '</p>', r'<a href=".*?">', '<s>', '</s>', r'http://twitter.com/search\?q=.*?&amp;src=hash',
        '<span>', '</span>', '</a>', '<b>', '</b>']

class TweetGetter(object):

    def parse_twitter(self):
        try:
            content = requests.get(self.url)
            if content.status_code == 404:
                raise requests.HTTPError
            print 'Connection successful!'
            soup = BeautifulSoup(content.text)

            self.title = soup.title.string
            self.tweets = []

            for content in soup.findAll("div", "content"):
                for meta, text in zip(content.findAll("small", "time"), content.findAll("p", "js-tweet-text tweet-text")):
                    self.tweets.append(Tweet(text, meta))
        except requests.HTTPError:
            print 'Error 404: Account not found'

    def to_rss(self, server=config.SERVER):
        try:
            with open(config.INSTALL_DIR + 'rss-model.tpl') as template_file:
                items = list(map(lambda tweet: tweet.to_jinja2(), self.tweets))
                try:
                    descriptor = self.hashtag
                    directory = 'htag'
                except AttributeError:
                    descriptor = self.username
                    directory = 'user'
                template = Template(template_file.read())
                return template.render(server=server, directory=directory, descriptor=descriptor, title=self.title, url=self.url, tweets=items)
        except IOError:
            return 'Template could not be open'


class UserTweetGetter(TweetGetter):
    def __init__(self, username, get_pics = False):
        self.username = username
        self.url = "https://twitter.com/{0}".format(self.username)

        self.parse_twitter()

class HashtagTweetGetter(TweetGetter):
    def __init__(self, hashtag, get_pics = False):
        self.hashtag = hashtag
        self.url = "https://twitter.com/search?q=%23{0}".format(self.hashtag)

        self.parse_twitter()
