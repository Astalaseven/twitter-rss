#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time

import twitter_rss

_logger = logging.getLogger(__name__)
config = twitter_rss.Config()


def main():
    feed_manager = twitter_rss.FeedManager(config)
    timer = config.getint('updater.timer', 600)
    try:
        while 1:
            _logger.info('Updating ALL THE FEEDS!')
            feed_manager.update_all_feeds()
            _logger.info('Wait for {} seconds'.format(timer))
            time.sleep(timer)
    except (KeyboardInterrupt, SystemExit):
        _logger.info('\nKeyboardInterrupt catched -- Finishing program.')

if __name__ == "__main__":
    config.logging_init()
    main()
