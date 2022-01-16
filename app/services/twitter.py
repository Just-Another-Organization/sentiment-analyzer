import tweepy

from models.Tweet import Tweet
from utils.configurator import get_twitter_configurations
from utils.logger import Logger


class Twitter:
    DATE_FORMAT = '%Y%m%d%H%M'

    def __init__(self):
        self.logger = Logger('Twitter')
        configurations = get_twitter_configurations()
        self.label_30_day = configurations['LABEL_30_DAY']
        auth = tweepy.OAuthHandler(configurations['CONSUMER_KEY'], configurations['CONSUMER_KEY_SECRET'])
        if configurations['USE_USER_CONTEXT']:
            self.logger.info('Using user context')
            auth.set_access_token(configurations['ACCESS_TOKEN'], configurations['ACCESS_TOKEN_SECRET'])
        else:
            self.logger.info('Skipping user context')

        self.api = tweepy.API(auth)

    def test(self):
        return self.search_recent(keyword='Tweepy')

    def search_recent(self, keyword, start_time=None, end_time=None):
        # Keyword match, only english
        query = keyword + ' lang:en'
        raw_tweets = self.api.search_30_day(
            label=self.label_30_day,
            query=query,
            fromDate=start_time.strftime(self.DATE_FORMAT),
            toDate=end_time.strftime(self.DATE_FORMAT))
        return Twitter.parse_tweets(raw_tweets)

    def search_popular_tweets(self, keyword, start_time=None, end_time=None):
        # Keyword match, no retweet, only english
        query = keyword + ' -is:retweet lang:en'
        raw_tweets = self.api.search_tweets(
            q=query,
            lang='en',
            result_type='popular')
        if start_time is not None and end_time is not None:
            return Twitter.filter_by_timeframe(raw_tweets, start_time, end_time)
        else:
            return Twitter.parse_tweets(raw_tweets)

    @staticmethod
    def filter_by_timeframe(raw_tweets, start_time, end_time):
        tweets = []
        for raw_tweet in raw_tweets:
            if start_time <= raw_tweet.created_at <= end_time:
                tweets.append(Tweet(raw_tweet))
        return tweets

    @staticmethod
    def parse_tweets(raw_tweets):
        return [Tweet(raw_tweet) for raw_tweet in raw_tweets]
