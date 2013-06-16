twitter-rss
===========

Rss-generator for Twitter

## Installation

    git clone git://github.com/Astalaseven/twitter-rss.git

    sudo apt-get install python-pip
    sudo pip install BeautifulSoup
    sudo pip install arrow
    
## Launch

You can edit twitter-rss.py file to change the time between two updates (TIMER = 60), the server name 
(SERVER = 'localhost') and the accounts you want to generate a RSS-feed for (ACCOUNTS = ['framasoft', 'aprilorg']).

    cd twitter-rss/
    python2 twitter-rss.py
