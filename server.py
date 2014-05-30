#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urlparse

from flask import Flask, render_template, request, redirect, url_for

import twitter_rss

app = Flask(__name__)
config = twitter_rss.Config()


@app.route('/')
def index():
    return render_template('index.tpl')


@app.errorhandler(404)
def page_not_found(code):
    err = 'User not found'
    error = render_template('index.tpl', err=err)
    return error


@app.route('/<kind>', methods=['POST'])
def handle_kind(kind):
    feed = request.form['user_data']
    return redirect(url_for('feed_to_xml', kind=kind, feed=feed))


@app.route('/<kind>/<feed>.xml')
def feed_to_xml(kind, feed):
    try:
        return twitter_rss.FeedManager(config).get(kind, feed)
    except OSError as e:
        return render_template('index.tpl', err="Can not create {0.filename}: {0.strerror}".format(e))
    except NotImplementedError as e:
        return render_template('index.tpl', err=e)


if __name__ == "__main__":
    config.logging_init()
    parsed_url = urlparse.urlparse(config.get('server.url'))
    app.run(
        host=parsed_url.hostname,
        port=parsed_url.port,
        debug=config.getbool('server.debug', False),
    )
