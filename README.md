twitter-rss
===========

Rss-generator for Twitter

* Doesn't make use of Twitter API (no registration needed, no 180 requests limitation, ...)
* Support account and hashtag following
* Option to append pic.twitter.com images in feed
* Generate a valid RSS-feed

## Installation

Requirements : `python2`

    git clone git://github.com/Astalaseven/twitter-rss.git

    sudo apt-get install python-pip
    sudo pip install BeautifulSoup
    sudo pip install arrow
    
## Launch

You can edit twitter-rss.py file to change the time between two updates (TIMER = 600), the server name 
(SERVER = 'localhost'), the accounts (ACCOUNTS = ['framasoft', 'UrLabBxl']) and the hashtags 
(HASHTAG = ['framasoft', 'urlab']) you want to generate a RSS-feed for.

    cd twitter-rss/
    python2 twitter-rss.py
