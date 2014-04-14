FROM ubuntu:latest

# Install prerequisites
RUN sed -i "s/main/main universe/" /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install git python-pip gunicorn supervisor

# Install pip requirements
RUN mkdir -p /home/asta/twitter-rss
WORKDIR /home/asta/twitter-rss
ADD requirements.txt /home/asta/twitter-rss/requirements.txt
RUN pip install -r requirements.txt

# Create data directories
RUN mkdir -p /var/www/twitter-rss
WORKDIR /var/www/twitter-rss
RUN mkdir -p user && touch user/user.txt
RUN mkdir -p htag && touch htag/htag.txt

# Add code from the current checkout
ADD . /home/asta/twitter-rss
# Alternatively, checkout the current master version from Github:
# RUN git clone git://github.com/Astalaseven/twitter-rss.git /home/asta/twitter-rss

# Expose port, set volume & start command
EXPOSE 5000
VOLUME /var/www/twitter-rss
CMD supervisord -n -c /home/asta/twitter-rss/supervisord.conf
