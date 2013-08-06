#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter_rss
import time
import config
import re

# Update the feeds
try:
    while 1:
        print 'Updating ALL THE FEEDS!'
        try:
            with open(config.XML_DIR + 'user/user.txt', 'r') as usernames:
                for user in usernames:
                    user = re.findall('(\w+) -- \d+', user)[0]
                    print(user)
                    twitter_rss.UserTweetGetter(user)
            usernames.close()

            with open(config.XML_DIR + 'htag/htag.txt', 'r') as hashtags:
                for htag in hashtags:
                    htag = re.findall('(\w+) -- \d+', htag)[0]
                    twitter_rss.HashtagTweetGetter(htag)
            hashtags.close()
        except IOError:
            print 'File could not be read'
        time.sleep(config.TIMER)

except (KeyboardInterrupt, SystemExit):
    print '\nKeyboardInterrupt catched -- Finishing program.'
