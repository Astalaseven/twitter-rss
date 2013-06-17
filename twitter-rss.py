#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import arrow
import time

### CONSTANTES ###
TIMER = 600
SERVER = 'localhost'
ACCOUNTS = ['framasoft', 'UrLabBxl']
HASHTAG = ['framasoft', 'urlab']
PICS = False

class TwitterToRss:

	def __init__(self, nick):
		self.tweets = []
		self.hashtag = []
		self.title = ''
		self.nick = nick
		self.server = SERVER

		self.initPseudo()
	
		self.clean()
		

	def initPseudo(self):

		if account:

			url = "https://twitter.com/{}".format(self.nick)

		elif hashtag:

			url = "https://twitter.com/search?q=%23{}&src=typd".format(self.nick)

		content = urllib2.urlopen(url)
		print 'Connection successful!'
		soup = BeautifulSoup(content)

		self.title = soup.title.string
		self.tweets = []
		pics = []

		for content in soup.findAll("div", "content"):

			for info, tweet in zip(content.findAll("small", "time"), content.findAll("p", "js-tweet-text tweet-text")):

				if PICS == True:
					self.tweets.append([info, tweet, pics])
				else:
					self.tweets.append([info, tweet])


	def printTweets(self):
		for tweet in self.tweets:
			print tweet

	def cleanTwit(self):
		to_delete = self.TWIT_DELETE

		to_replace = [{'<s>@</s>': '@'},
					  {'href="/': 'href="http://twitter.com/'}]

		for i, tweet in enumerate(self.tweets):
			for item in to_delete:
				self.tweets[i][1] = re.sub(item, '', str(self.tweets[i][1]))
			for item in to_replace:
				for old, new in item.items():
					self.tweets[i][1] = re.sub(
						old, new, str(self.tweets[i][1]))

	def cleanInfo(self):
		for i, tweet in enumerate(self.tweets):

			soup = BeautifulSoup(str(self.tweets[i][0]))
			for href in soup.findAll('a'):

				link = re.sub(r'\(u\'href\', u\'(.*)\'\)', r'\1', str(
					href.attrs[0]))

				tmp = soup.find('span')
				date = re.sub(r'\(u\'data-time\', u\'(.*)\'\)', r'\1', str(
					tmp.attrs[1]))

				plop = str(self.tweets[i][1])

				self.tweets[i][0] = [link, date, plop]

	def cleanTweet(self):
		to_delete = self.TWEET_DELETE
		for i, clean_twit in enumerate(self.tweets):
			for item in to_delete:

				self.tweets[i][0][2] = re.sub(
					item, '', str(self.tweets[i][0][2]))
	

	def cleanTimestamp(self):
		for i, tweet in enumerate(self.tweets):
			timestamp = arrow.Arrow.fromtimestamp(float(self.tweets[i][0][1]))
			date = timestamp.strftime('%a, %d %b %Y %H:%M:%S %z')
			self.tweets[i][0][1] = date

	def generateHtml(self):
		with open(self.nick + '.html', 'w') as html:
			html.write(
				'<meta http-equiv="Content-type" content="text/html; charset=UTF-8"/>\n\n')
			for tweet in self.tweets:

				html.write(str(tweet[1]) + '\n\n')

		html.close()

	def backupTweet(self):
		update = True
		data = ''
		try:
			with open(self.nick + '-backup.xml', 'r') as original:
				first_tweet = []
				first_tweet.append(original.readline())
				if first_tweet[0]:
					first_tweet = first_tweet[0].split('\'')[1]

					for i, tweet in enumerate(self.tweets):
						if first_tweet in self.tweets[i][0][0]:
							update = False
							data = original.read()

		except IOError:
			print 'Error: The file ' + self.nick + '-backup.xml could not be read'
			pass

		if update:
			with open(self.nick + '-backup.xml', 'w') as modified:
				print 'Update in progress'

				for tweet in self.tweets:
					modified.write(str(tweet) + '\n\n')
				modified.write(str(data))
				print 'Update done'
		else:
			print self.nick + ': Already updated, nothing to do'

	def generateRss(self):

		if not account:
			self.nick = self.nick + '-search'

		with open(self.nick + '.xml', 'w') as html:

			html.write(self.XML_TOP.format(
				nick=self.nick, title=self.title, server=self.server))

			for i, item in enumerate(self.tweets):

				date = str(self.tweets[i][0][1])
				link = str(self.tweets[i][0][0])
				twit = str(self.tweets[i][1])
				title = str(self.tweets[i][0][2])
				author = str(self.tweets[i][0][0]).split('/')[1]

				html.write(self.XML_FOR.format(
					title=title, link=link, date=date, twit=twit, author=author))


				if PICS == True and self.tweets[i][2]:

					img = self.tweets[i][2][0]
					alt = self.tweets[i][2][1]

					html.write(self.XML_IMG.format(
						img = img, title = title))

				html.write(self.XML_ITEM)

			html.write(self.XML_END)
		html.close()

	def isRssValid(self):

		url = "http://validator.w3.org/feed/check.cgi?url={}/{}.xml".format(self.server, self.nick)
		print url
		content = urllib2.urlopen(url)
		soup = BeautifulSoup(content)
		response = soup.findAll("span", { "class" : "message" })[0].text
		print response

	def activatePics(self):
		for i, item in enumerate(self.tweets):
			tweet = str(self.tweets[i][1])
			if 'pic.twitter.com' in tweet:
				url = re.findall(r'(\S+.com/\S+)', tweet)
				for j in url:
					if 'pic.twitter.com' in j:
						url = 'http://' + str(re.sub(r'.*pic.twitter.com/(\S+)</a>.*', r'pic.twitter.com/\1', j))
						content = urllib2.urlopen(url)
						soup = BeautifulSoup(content)
						pics = re.findall(r'(https?://pbs.twimg.com/media/\S+.jpg:large)', str(soup))
						title = soup.title.string
						self.tweets[i][2] = [pics[0], title]


	def clean(self):
		self.cleanTwit()
		self.cleanInfo()
		self.cleanTimestamp()
		self.cleanTweet()

	TWIT_DELETE = [
		' class="js-tweet-text tweet-text"',
		' class="twitter-atreply pretty-link"',
		' class="invisible"',
		' class="js-display-url"',
		' class="twitter-hashtag pretty-link js-nav"',
		' class="twitter-timeline-link"',
		' class="tco-ellipsis"',
		' class="invisible"',
		' data-query-source="hashtag_click"',
		' rel="nofollow"',
		' target="_blank"',
		' data-expanded-url=".*?"',
		' title=".*?"',
		' data-query-source="hashtag_click"',
		' dir="ltr"',
		'<span><span>&nbsp;</span>.*</span>',
		'<span>http://</span>',
		' data-pre-embedded="true"',
		'<p>', '</p>', '<span>', '</span>', '<strong>', '</strong>']

	TWEET_DELETE = [
		'<p>', '</p>', r'<a href=".*?">', '<s>', '</s>', r'http://twitter.com/search\?q=.*?&amp;src=hash',
		'<span>', '</span>', '</a>', '<b>', '</b>']

	XML_TOP = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
	<channel>
		<atom:link href="http://{server}/{nick}.xml" rel="self" type="application/rss+xml" />
		<title>{title}</title>
		<link>https://twitter.com/{nick}</link>
		<description>twitter-rss of {nick}</description>
		<language>fr</language>

		'''

	XML_FOR = '''
				<item>
				<title>{author}: {title}</title>
				<guid>https://twitter.com{link}</guid>
				<link>https://twitter.com{link}</link>
				<pubDate>{date}</pubDate>
				<description><![CDATA[{author}: {twit}'''

	XML_IMG = '''
				<img src="{img}" alt="{title}" style="max-width: 50%; height: 50%;"/>
				'''
				
	XML_ITEM = ''']]></description>
				</item>
				'''

	XML_END = '''
	</channel>
</rss>'''


if __name__ == '__main__':

	while i:

		print arrow.utcnow().to('Europe/Brussels').format('YYYY-MM-DD HH:mm:ss')
		
		if ACCOUNTS:

			for account in ACCOUNTS:

				hashtag = False

				try:
					tweet = TwitterToRss(account)
					print 'Account {account} found'.format(account=account)
					error = 200
				except urllib2.HTTPError as e:
					if e.code == 404:
						print 'Account {account} not found'.format(account=account)
						error = e.code
						print 'Error: Twitter returned {error} for {account}'.format(error=error, account=account)
					elif e.code == 101:
						print 'Error: Network is unreachable'
				except urllib2.URLError as e:
					print 'Invalid URL'
					error = -2

				if error == 200:
					if PICS == True:
						tweet.activatePics()
					tweet.generateHtml()
					
					tweet.generateRss()

					tweet.backupTweet()
					# tweet.isRssValid()
		else:
			print('Not account specified')

		if HASHTAG:

			for hashtag in HASHTAG:

				account = False

				try:
					tweet = TwitterToRss(hashtag)
					print 'Hashtag {hashtag} found'.format(hashtag=hashtag)
					error = 200
				except urllib2.HTTPError as e:
					if e.code == 404:
						print 'Hashtag {hashtag} not found'.format(hashtag=hashtag)
						error = e.code
						print 'Error: Twitter returned {error} for {hashtag}'.format(error=error, hashtag=hashtag)
					elif e.code == 101:
						print 'Error: Network is unreachable'
				except urllib2.URLError as e:
					print 'Invalid URL'
					error = -2

				if error == 200:
					if PICS == True:
						tweet.activatePics()
					tweet.generateHtml()
					
					tweet.generateRss()

					tweet.backupTweet()
					# tweet.isRssValid()
		else:
			print('Not hashtag specified')

		time.sleep(TIMER)

# tweet.printTweets()
