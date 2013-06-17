from flask import Flask
import time
import twitter_rss

app = Flask(__name__)

@app.route("/")
def hello():
	return "Goto domain.com/twitterusername.xml"

@app.route('/<username>.xml')
def twitter_to_xml(username):

	try:
		with open('accounts.txt', 'r') as check_accounts:
			check = check_accounts.read()
			if username in check:
				write = False
		check_accounts.close()

		if write:
			with open('accounts.txt', 'a') as usernames:
				usernames.write(username + '\n')
			usernames.close()

		twitter_rss.TwitterToRss(username)

		# print 'Waiting 10 seconds before feed is generated...'
		# #time.sleep(15)

		with open(username + '.xml', 'r') as content_file:
			content = content_file.read()
		content_file.close()

		return content 
	except IOError:
		return 'File could not be read'

if __name__ == "__main__":
	app.run(debug=True)