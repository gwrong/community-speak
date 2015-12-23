from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time



class StdOutListener(StreamListener):

    def __init__(self, seconds):
        self.outputFile = open('text/tweets.txt', 'w')
        self.startTime = time.time()
        self.seconds = seconds

    def on_data(self, data):
        self.outputFile.write(data + '\n')
        currentTime = time.time()
        if (currentTime - self.startTime < self.seconds):
            return True
        else:
            return False

    def on_error(self, status):
        print(status)

'''
Gather tweets with they keywords for the number of seconds
'''
def getTweets(keywords, seconds):

    startTime = time.time()
    currentTime = time.time()

    print("Getting Tweets")
    listener = StdOutListener(seconds)

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=keywords)

def getTweetText():
    inputFile = open('text/tweets.txt', 'r')
    outputFile = open('text/tweetsText.txt', 'w')
    for line in inputFile:
        try:
            tweet = json.loads(line)
            outputFile.write(tweet['text'] + '\n')
        except:
            continue
if __name__ == '__main__':
    getTweets(['Donald Trump'], 7200)
    getTweetText()