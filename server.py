#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import time
import twitter_rss
# from jinja2 import Template
host = 'localhost:5000'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.tpl')



@app.route('/user', methods=['POST'])
def handle_user():
    feed = request.form['user_data']
    return redirect(url_for('user_to_xml', feed=feed))

@app.route('/htag', methods=['POST'])
def handle_htag():
    feed = request.form['user_data']
    return redirect(url_for('hashtag_to_xml', feed=feed))


@app.route('/user/<feed>.xml')
def user_to_xml(feed):
    try:
        with open('user/' + feed + '.xml') as tweets:
            tweets = tweets.read()
            return tweets
    except IOError:
        print 'File does not exist: Creating feed...'

        tweets = twitter_rss.UserTweetGetter(feed)
        with open('user/' + feed + '.xml', 'w') as cache:
            cache.write(tweets.to_rss().encode('utf-8'))
        cache.close()

        return tweets.to_rss()

@app.route('/htag/<feed>.xml')
def hashtag_to_xml(feed):
    try:
        with open('htag/' + feed + '.xml') as tweets:
            tweets = tweets.read()
            return tweets
    except IOError:
        print 'File does not exist: Creating feed...'

        tweets = twitter_rss.HashtagTweetGetter(feed)
        with open('htag/' + feed + '.xml', 'w') as cache:
            cache.write(tweets.to_rss().encode('utf-8'))
        cache.close()

        return tweets.to_rss()

# @app.route('/feed', methods=['POST'])
# def handle_username():
#     try:
#         return redirect(url_for('twitter_to_xml', username=request.form['rss']))
#     except:
#         return redirect(url_for('hashtag_to_xml', hashtag=request.form['rss']))


# @app.route('/<username>.xml')
# def twitter_to_xml(username):
#     try:
#         with open(username + '.xml') as tweets:
#             tweets = tweets.read()
#             return tweets
#     except IOError:
#         print 'File does not exist: Creating feed...'

#         tweets = twitter_rss.UserTweetGetter(username)
#         with open(username + '.xml', 'w') as cache:
#             cache.write(tweets.to_rss().encode('utf-8'))
#         cache.close()

#         return tweets.to_rss()

# @app.route('/tag-<hashtag>.xml')
# def hashtag_to_xml(hashtag):
#     try:
#         with open('tag-' + hashtag + '.xml') as tweets:
#             tweets = tweets.read()
#             return tweets
#     except IOError:
#         print 'File does not exist: Creating feed...'

#         tweets = twitter_rss.HashtagTweetGetter(hashtag)
#         with open('tag-' + hashtag + '.xml', 'w') as cache:
#             cache.write(tweets.to_rss().encode('utf-8'))
#         cache.close()
    
#     return tweets.to_rss()

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))
    # error = 'Account or hashtag not found!'
    # return render_template('index.tpl', error=error)

@app.errorhandler(500)
def page_not_found(error):
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0')
    # app.run()