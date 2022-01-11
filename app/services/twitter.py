import tweepy

from utils.configurator import get_twitter_configurations
from utils.logger import Logger


class Twitter:
    def __init__(self):
        self.logger = Logger('Twitter')
        configurations = get_twitter_configurations()
        self.client = tweepy.Client(bearer_token=configurations['BEARER_TOKEN'])

    def test(self):
        return self.search(keyword='Tweepy', limit=2)

    def search(self, keyword, limit=100, start_time=None, end_time=None):
        # Keyword match, no ads, no retweet, only english
        query = keyword + ' -is:retweet lang:en'
        tweets = self.client.search_recent_tweets(
            query=query,
            tweet_fields=['text', 'id', 'organic_metrics'],
            max_results=limit,
            start_time=start_time,
            end_time=end_time)
        return tweets.data
