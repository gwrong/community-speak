from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

#tokens here

class StdOutListener(StreamListener):

    def __init__(self):
        self.outputFile = open('text/tweets.txt', 'w')

    def on_data(self, data):
        self.outputFile.write(data + '\n')
        return True

    def on_error(self, status):
        print(status)

def getTweets(keywords):
    print("Getting Tweets")
    listener = StdOutListener()

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
    #getTweets(['Donald Trump'])
    getTweetText()