twitter-rss
===========

Rss-generator for Twitter

* Doesn't make use of Twitter API (no registration needed, no 180 requests limitation, ...)
* Support account and hashtag following
* Option to append pic.twitter.com images in feed [in dev]
* Generate a valid RSS-feed

## Installation

Requirements : `python2`

    git clone git://github.com/Astalaseven/twitter-rss.git

    sudo apt-get install python-pip
    sudo pip install BeautifulSoup
    sudo pip install arrow
    sudo pip install flask
    
## Launch

You can edit `config.py` file to change the time between two updates (TIMER = 600),the server name 
(SERVER = 'localhost:5000') and where the files should be stocked (DIR = '/var/www/').

    cd twitter-rss/
    python2 run.py
  
`run.py` will launch a webserver that can be used to create new feeds. You can also create them by opening 
`your_server/user/choosen-user-or-hashtag.xml` or by directly write them down in `user/user.txt` and `htag/htag.txt`.
