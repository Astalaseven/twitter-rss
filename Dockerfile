FROM ubuntu:latest

RUN sed -i "s/main/main universe/" /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install git python-pip

RUN git clone git://github.com/Astalaseven/twitter-rss.git
RUN cd twitter-rss && pip install -r requirements.txt

RUN sed -i "s/INSTALL_DIR.*/INSTALL_DIR = '\/twitter-rss\/'/" /twitter-rss/config.py
RUN mkdir -p /var/www/twitter-rss/user
RUN mkdir -p /var/www/twitter-rss/htag

EXPOSE 5000

CMD cd twitter-rss && python2 run.py
