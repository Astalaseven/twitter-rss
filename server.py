#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import twitter_rss
import config

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
        with open(config.XML_DIR + path + '/' + feed + '.xml') as tweets:
            tweets = tweets.read()
            if not tweets:
                err = 'Cache is empty'
                error = render_template('index.tpl', err=err)
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
            err = 'User not found'
            error = render_template('index.tpl', err=err)
        write_data_to_file(tweets, feed, path)
        save_feed_for_updating(feed, path)
    return error
           
def write_data_to_file(tweets, feed, path):
    err=None
    try:
        data = tweets.to_rss().encode('utf-8')
        print 'File does not exist: Creating feed...'
        with open(config.XML_DIR + path + '/' + feed + '.xml', 'w') as cache:
            cache.write(data)
        cache.close()
        error = tweets.to_rss()
    except IOError:
        err = 'File could not be written'
    except AttributeError:
        err = 'User not found'
    error = render_template('index.tpl', err=err)
    return error

def save_feed_for_updating(feed, path):
    try:
        with open(config.XML_DIR + path + '/' + path + '.txt', 'a') as save:
            save.write(feed + '\n')
        save.close()
    except IOError:
        print 'Could not save ' + feed + ' in ' + path


@app.errorhandler(404)
def page_not_found(code):
    err = 'User not found'
    error = render_template('index.tpl', err=err)
    return error


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0')
    # app.run()
