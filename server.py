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
    tweets = twitter_rss.UserTweetGetter(username)
    return tweets.to_rss()


if __name__ == "__main__":
    app.run(debug=True)