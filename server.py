#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import config
import re
import requests
import twitter_rss

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
    if check_if_new_tweet(feed, path) is False:
        error = serve_from_cache(feed, path)
    else:
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
        save_feed_for_updating(tweets, feed, path)
    return error

def find_new_first_id(feed, path):
    if path == 'user':
        url = "https://mobile.twitter.com/{0}"
    else:
        url = "https://mobile.twitter.com/search?q=%23{0}"
    content = requests.get(url.format(feed))
    content = content.text.encode('utf-8')
    try:
        new_first_id = re.findall(r'data-id="(\d+)"', str(content))[0]
    except IndexError:
        new_first_id = "42"
    return new_first_id

def find_old_first_id(txt_file, feed):
    old_first_id = ''
    try:
        with open(txt_file, 'r') as f:
            content = f.read()
            old_first_id = re.findall("{0} -- (\d+)".format(feed), content)[0]
    except IndexError:
        pass
    return old_first_id

def update_id_in_txt_file(txt_file, feed, new_first_id):
    with open(txt_file, 'r') as f:
            content = f.read()
    with open(txt_file, 'w') as m:
        update = re.sub("{0} -- \d+".format(feed), "{0} -- {1}".format(feed, new_first_id), content)
        m.write(update)

def check_if_new_tweet(feed, path):
    print('Checking if new tweet for {0}...'.format(feed))
    update = True
    txt_file = config.XML_DIR + path + '/' + path + '.txt'
    new_first_id = find_new_first_id(feed, path)
    old_first_id = find_old_first_id(txt_file, feed)
    if new_first_id == old_first_id:
        update = False
    else:
        update_id_in_txt_file(txt_file, feed, new_first_id)
    return update

def serve_from_cache(feed, path):
    error = ''
    try:
        with open(config.XML_DIR + path + '/' + feed + '.xml') as tweets:
            tweets = tweets.read()
            if not tweets:
                err = 'Cache is empty'
                error = render_template('index.tpl', err=err)
            else:
                print('Serving feed from cache')
                error = tweets
    except IOError:
        print('Could not write the feed cache')
    return error
           
def write_data_to_file(tweets, feed, path):
    err=None
    try:
        data = tweets.to_rss().encode('utf-8')
        print 'File does not exist: Creating feed...'
        with open(config.XML_DIR + path + '/' + feed + '.xml', 'w') as cache:
            cache.write(data)
        error = tweets.to_rss()
    except IOError:
        err = 'File could not be written'
    except AttributeError:
        err = 'User not found'
    error = render_template('index.tpl', err=err)
    return error

def save_feed_for_updating(tweets, feed, path):
    new_first_id = find_new_first_id(feed, path)
    try:
        with open(config.XML_DIR + path + '/' + path + '.txt', 'a') as save:
            save.write(feed + ' -- ' + new_first_id + '\n')

    except IOError:
        print 'Could not save ' + feed + ' in ' + path


@app.errorhandler(404)
def page_not_found(code):
    err = 'User not found'
    error = render_template('index.tpl', err=err)
    return error


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0')
    # app.run()
