#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter_rss
import time
import subprocess
import config
import sys

# Launch web server
p = subprocess.Popen([sys.executable, config.INSTALL_DIR + 'server.py'])

# Update the feeds
try:
    while 1:
        print 'Updating ALL THE FEEDS!'
        try:
            with open(config.XML_DIR + 'user/user.txt', 'r') as usernames:
                for user in usernames:
                    twitter_rss.UserTweetGetter(user)
            usernames.close()

            with open(config.XML_DIR + 'htag/htag.txt', 'r') as hashtags:
                for htag in hashtags:
                    twitter_rss.HashtagTweetGetter(user)
            hashtags.close()
        except IOError:
            print 'File could not be read'
        time.sleep(config.TIMER)

except (KeyboardInterrupt, SystemExit):
    p.kill() # kill the subprocess
    print '\nKeyboardInterrupt catched -- Finishing program.'
