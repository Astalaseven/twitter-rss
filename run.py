import twitter_rss
import time
import subprocess

# Launch web server
p = subprocess.Popen(['/usr/bin/python2', 'server.py'])

# Update the feeds
while 1:
	print 'Updating ALL THE FEEDS!'
	try:
		with open('user/user.txt', 'r') as usernames:
			for user in usernames:
				twitter_rss.UserTweetGetter(user)
		usernames.close()

		with open('htag/htag.txt', 'r') as hashtags:
			for htag in hashtags:
				twitter_rss.HashtagTweetGetter(user)
		hashtags.close()
	except IOError:
		print 'File could not be read'
	time.sleep(600)

p.kill() # kill the subprocess