import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# API credentials
consumer_key = '<consumer key>'
consumer_secret = '<consumer secret>'
access_key = '<access key>'
access_secret = '<access secret>'

# API authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# Initialise Vader sentiment analyser
analyzer = SentimentIntensityAnalyzer()


class MyStreamListener(tweepy.StreamListener):
	"""
	A Twitter listener that build on Tweepy's Stream Listener,
	performing Vader sentiment analysis on each new tweet for a given
	hashtag and graphing the results live.

	Attributes:
		scores -- a list of polarity scores, one per tweet
		tweet_count (int) -- a count of the no. of tweets analysed 
	"""
	scores = []
	tweet_count = 0

	def on_status(self, status):
		# Print count of tweets viewed
		self.tweet_count += 1
		print('---' + str(self.tweet_count) + '---')

		# Print tweet and perform sentiment analysis
		print(status.text)
		self.scores.append(analyzer.polarity_scores(status.text)['compound'])
		
		# Add polarity score and plot
		plt.plot(self.scores)
		plt.draw()
		plt.pause(0.5)
		plt.clf()

		# # Write tweet to file
		# with open('tweets.txt', 'a') as f:
		# 	f.write(status.text + '\n-break-\n')

	def on_error(self, status):
		print(status)


# Create stream listener
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# Start stream
myStream.filter(track=['#blm'], languages=['en'])