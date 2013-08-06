twitter-rss
===========

Rss-generator for Twitter

* Doesn't make use of Twitter API (no registration needed, no 180 requests limitation, ...)
* Support account and hashtag following
* Option to append pic.twitter.com images in feed
* Generate a valid RSS-feed

A running instance is available here: https://wtf.roflcopter.fr/twitter-rss/ 
on PoGo606's server (https://wtf.roflcopter.fr/links/pogo). 

The theme can be found here:
https://github.com/PoGo606/twitter-rss/commit/9835654ac549b01b76d4a87cf9e4c096578b30f2

Default theme: ![ScreenShot](http://i.imgur.com/slSbJBO.png)
Pogo's theme: ![ScreenShot](http://i.imgur.com/i9bv24r.png)

## Installation

Requirements : `python2`

    sudo apt-get install git python-pip
    
    git clone git://github.com/Astalaseven/twitter-rss.git    
    sudo pip install -r requirements.txt

### Creating folders to store the feeds

    sudo mkdir -p /var/www/twitter-rss/     # default XML_DIR in config.py
    cd /var/www/twitter-rss/
    sudo mkdir user/ && sudo touch user/user.txt
    sudo mkdir htag/ && sudo touch htag/htag.txt

### Setting right permissions

    sudo chown your_username:www-data -R /var/www/twitter-rss
    sudo chmod 0755 -R /var/www/twitter-rss

    
## Launch

You can edit `config.py` file to change the time between two updates (`TIMER = 600`), where the files should be stocked (`DIR = '/var/www/'`) and if you want to fetch the tweet pic (`PICS = False`).

The server name must be set to have a valid RSS feed (`SERVER = 'localhost:5000'`).

    cd twitter-rss/
    python2 server.py

### Using Gunicorn and Supervisor (recommended)

#### Installing packages

    sudo apt-get install gunicorn supervisor

Modify `supervisord.conf` to reflect your installation:

    directory=/home/asta/twitter-rss/    # directory where `server.py` is located

You can check if `supervisor` works well:

    sudo supervisord -n -c ~/twitter-rss/supervisord.conf

and place it in the right place to be launch on startup:

    sudo mv ~/twitter-rss/supervisord.conf /etc/supervisor/


Gunicorn will launch a webserver that can be used to create new feeds, and launch a script to update the feeds. 

Supervisor is set to check all scripts are running or as they need to be relaunched.

### Creating a feed

If the webserver is running, you can create a feed by: 

* using the web form served by Gunicorn (`http://your_server:8000/),
* opening `http://your_server/user/choosen-user.xml` or `http://you_server/htag/choosen-hashtag`,
* writing them down in `user/user.txt` and `htag/htag.txt`.

### Use a different port

If you want to launch `twitter-rss` on a different port than Gunicorn's default (8000), you need to edit the `supervisord.conf` file to:

    command=/usr/bin/gunicorn --bind=0.0.0.0:5000 server:app  # where 5000 is the new port


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
