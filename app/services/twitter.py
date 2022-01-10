import tweepy

from utils.configurator import get_twitter_configurations
from utils.logger import Logger


class Twitter:
    def __init__(self):
        self.logger = Logger('Twitter')
        configurations = get_twitter_configurations()
        auth = tweepy.AppAuthHandler(configurations['API_KEY'], configurations['API_KEY_SECRET'])
        self.api = tweepy.API(auth)

    def test(self):
        for tweet in tweepy.Cursor(self.api.search_tweets, q='tweepy').items(10):
            self.logger.info(tweet.text)

    def search(self, keyword, limit=100):
        return tweepy.Cursor(self.api.search_tweets, q=keyword).items(limit)
