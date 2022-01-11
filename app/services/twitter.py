import tweepy

from utils.configurator import get_twitter_configurations
from utils.logger import Logger


class Twitter:
    def __init__(self):
        self.logger = Logger('Twitter')
        configurations = get_twitter_configurations()
        self.client = tweepy.Client(
            consumer_key=configurations['CONSUMER_KEY'],
            consumer_secret=configurations['CONSUMER_KEY_SECRET'],
            access_token=configurations['ACCESS_TOKEN'],
            access_token_secret=configurations['ACCESS_TOKEN_SECRET'])

    def test(self):
        return self.search(keyword='Tweepy', limit=2)

    def search(self, keyword, limit=100, start_time=None, end_time=None):
        # Keyword match, no ads, no retweet, only english
        query = keyword + ' -is:retweet lang:en'
        tweets = self.client.search_recent_tweets(
            query=query,
            tweet_fields=['text', 'id', 'public_metrics'],
            max_results=limit,
            start_time=start_time,
            end_time=end_time,
            user_auth=True)
        return tweets.data
