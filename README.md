twitter-rss
===========

Rss-generator for Twitter

* Doesn't make use of Twitter API (no registration needed, no 180 requests limitation, ...)
* Support account and hashtag following
* Option to append pic.twitter.com images in feed
* Generate a valid RSS-feed

## Installation

Requirements : `python2`

    sudo apt-get install git python-pip
    
    git clone git://github.com/Astalaseven/twitter-rss.git    
    sudo pip install -r requirements.txt
    
## Launch

You can edit `config.py` file to change the time between two updates (TIMER = 600),the server name 
(SERVER = 'localhost:5000'), where the files should be stocked (DIR = '/var/www/') and if you want 
to fetch the tweet pic (PICS = False).

    cd twitter-rss/
    python2 run.py
  
`run.py` will launch a webserver that can be used to create new feeds. You can also create them by opening 
`your_server/user/choosen-user-or-hashtag.xml` or by directly write them down in `user/user.txt` and `htag/htag.txt`.

## Daemon

A daemon script is not available to be run on Debian-like system (tested on Ubuntu 13.04) thanks to [PoGo606] [3].

    sudo mkdir -p /var/log/twitter-rss
    sudo mkdir -p /var/www/twitter-rss
    cd /var/www/twitter-rss
    sudo chmod +x twitter-rss.init.d.debian
    sudo chmod +x run.py
    sudo touch /var/log/twitter-rss/twitter-rss.log
    sudo chmod 640 /var/log/twitter-rss/twitter-rss.log
    sudo ./twitter-rss.init.d.debian start

You also need to change the `INSTALL_DIR` variable in `config.py` to be the same as `TWRSS_DIR` variable in `twitter-rss.init.d.debian`.

If the server doesn't run, try to remove the `--background` option in `twitter-rss.init.d.debian` to debug.

## Docker way

Thanks to [djmaze] [1], it is now possible to run `twitter-rss` using [Docker] [2].

Explanations on how to get it working are here: http://www.docker.io/gettingstarted/
(Docker only works on 64bit systems for now)

[1]: https://github.com/djmaze "djmaze"
[2]: http://docker.io "Docker.io"
[3]: https://github.com/PoGo606/twitter-rss/b44b0f6b0c8630fa83b46148702f05b55664935b/tools/twitter-rss.init.d.debian
