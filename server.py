#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import time
import twitter_rss

app = Flask(__name__)

@app.route("/")
def hello():
    return "Goto domain.com/twitterusername.xml"

@app.route('/<username>.xml')
def twitter_to_xml(username):
    try:
        with open(username + '.xml') as tweets:
            tweets = tweets.read()
            return tweets
    except IOError:
        print 'File does not exist: Creating feed...'

        tweets = twitter_rss.UserTweetGetter(username)
        with open(username + '.xml', 'w') as cache:
            cache.write(tweets.to_rss().encode('utf-8'))
        cache.close()

        return tweets.to_rss()

@app.route('/tag-<username>.xml')
def hashtag_to_xml(username):
    tweets = twitter_rss.HashtagTweetGetter(username)
    return tweets.to_rss()


if __name__ == "__main__":
    app.run(debug=True)