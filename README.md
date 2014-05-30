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
```
sudo apt-get install git python-pip
    
git clone git://github.com/Astalaseven/twitter-rss.git
sudo pip install -r requirements.txt
```

## Launch

You can edit `local_settings.ini` file to change settings (use settings.ini as template, `local_settings.ini` will not be overwritten on update).
```
cd twitter-rss/
python2 server.py
```

### Using Gunicorn and Supervisor (recommended)

#### Installing packages
```
sudo apt-get install gunicorn supervisor
```

Modify `supervisord.conf` to reflect your installation:
```
directory=/home/asta/twitter-rss/    # directory where `server.py` is located
```

You can check if `supervisor` works well:
```
sudo supervisord -n -c ~/twitter-rss/supervisord.conf
```
and place it in the right place to be launch on startup:
```
sudo mv ~/twitter-rss/supervisord.conf /etc/supervisor/
```

Gunicorn will launch a webserver that can be used to create new feeds, and launch a script to update the feeds. 

Supervisor is set to check all scripts are running or if needed relaunch them. Ubuntu should automatically launch it on startup.

### Creating a feed

If the webserver is running, you can create a feed by: 

* using the web form served by Gunicorn (`http://your_server:5000/`),
* opening `http://your_server:5000/user/choosen-user.xml` or `http://your_server:5000/htag/choosen-hashtag`,
* writing them down in `user/user.txt` and `htag/htag.txt`.

### Use a different port

If you want to launch `twitter-rss` on a different port than Gunicorn's default (8000), you need to edit the `supervisord.conf` file to:
```
command=/usr/bin/gunicorn --bind=0.0.0.0:5000 server:app  # where 5000 is the new port
```

`supervisord.conf` is already configured to use Gunicorn on port 5000.


## Daemon

A daemon script is now available to be run on Debian-like system (tested on Ubuntu 13.04) thanks to [PoGo606] [1].
```
sudo mkdir -p /var/log/twitter-rss
sudo mkdir -p /var/www/twitter-rss
cd /var/www/twitter-rss
sudo chmod +x twitter-rss.init.d.debian
sudo chmod +x run.py
sudo touch /var/log/twitter-rss/twitter-rss.log
sudo chmod 640 /var/log/twitter-rss/twitter-rss.log
sudo ./twitter-rss.init.d.debian start
```

You also need to change the `INSTALL_DIR` variable in `config.py` to be the same as `TWRSS_DIR` variable in `twitter-rss.init.d.debian`.

If the server doesn't run, try to remove the `--background` option in `twitter-rss.init.d.debian` to debug.

## Docker way

Thanks to [djmaze] [2], it is now possible to run `twitter-rss` using [Docker] [3].

Explanations on how to get docker working are here: http://www.docker.io/gettingstarted/
(Docker only works on 64bit systems for now)

After installing docker, you can build the docker image and run it:
```
sudo docker build -t twitter-rss .
sudo docker run -d -p 5000:5000 twitter-rss
```

Or use [fig] [4]:
```
sudo fig up -d
```

## The Heroku way
1. Install Heroku-toolbelt
1. Configure your account `heroku login`

```
heroku create <app-name>
git push heroku master  # upload your application to Heroku
heroku open  # Open your application in your browser
```

[1]: https://github.com/PoGo606/twitter-rss/b44b0f6b0c8630fa83b46148702f05b55664935b/tools/twitter-rss.init.d.debian
[2]: https://github.com/djmaze "djmaze"
[3]: http://docker.io "Docker.io"
[4]: http://orchardup.github.io/fig/
