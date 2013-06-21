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
    path = request.path
    return redirect(url_for('feed_to_xml', feed=feed, path=path))

@app.route('/htag', methods=['POST'])
def handle_htag():
    feed = request.form['user_data']
    path = request.path
    return redirect(url_for('feed_to_xml', feed=feed, path=path))


@app.route('/<path>/<feed>.xml')
def feed_to_xml(feed, path):
    try:
        with open(path + '/' + feed + '.xml') as tweets:
            tweets = tweets.read()
            if not tweets:
                error = redirect(url_for('index'))
            else:
                error = tweets
    except IOError:
        try:
            if path == 'user':
                tweets = twitter_rss.UserTweetGetter(feed)
            elif path == 'htag':
                tweets = twitter_rss.HashtagTweetGetter(feed)
            error = tweets.to_rss().encode('utf-8')
        except AttributeError:
            error = redirect(url_for('index'))
        write_data_to_file(tweets, feed, path)
        save_feed_for_updating(feed, path)      
    return error
           
def write_data_to_file(tweets, feed, path):
    try:
        data = tweets.to_rss().encode('utf-8')
        print 'File does not exist: Creating feed...'
        with open(path + '/' + feed + '.xml', 'w') as cache:
            cache.write(data)
        cache.close()
        error = tweets.to_rss()
    except IOError:
        error = 'File could not be written'
    except AttributeError:
        error = redirect(url_for('index'))

def save_feed_for_updating(feed, path):
    try:
        with open(path + '/' + path + '.txt', 'a') as save:
            save.write(feed + '\n')
        save.close()
    except IOError:
        print 'Could not save ' + feed + ' in ' + path



@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0')
    # app.run()