#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time

import config
import twitter_rss

_logger = logging.getLogger(__name__)


def main():
    feed_manager = twitter_rss.FeedManager()
    try:
        while 1:
            _logger.info('Updating ALL THE FEEDS!')
            feed_manager.update_all_feeds()
            _logger.info('Wait for {} seconds'.format(config.TIMER))
            time.sleep(config.TIMER)
    except (KeyboardInterrupt, SystemExit):
        _logger.info('\nKeyboardInterrupt catched -- Finishing program.')

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
