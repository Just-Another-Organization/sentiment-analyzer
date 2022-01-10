import utils.costants as label
import utils.utilities as utilities
from services.sentiment_analyzer import SentimentAnalyzer
from services.tester import Tester
from services.twitter import Twitter
from utils.logger import Logger


class Core:

    def __init__(self):
        self.logger = Logger('Core')
        self.analyzer = SentimentAnalyzer()
        self.twitter = Twitter()

    def test(self):
        tester = Tester(self.analyzer)
        tester.test()
        self.twitter.test()
        del tester

    def test_dataset(self):
        tester = Tester(self.analyzer)
        tester.test_dataset()
        del tester

    def analyze_keywords(self, keywords):
        result = {}
        for word in keywords:
            tweets = self.twitter.search(keyword=word, limit=100)
            negative_tweets = 0
            neutral_tweets = 0
            positive_tweets = 0

            for tweet in tweets:
                text = str(tweet.text)
                tweet_sentiment = self.analyzer.analyze_sentiment(text)['sentiment']
                if tweet_sentiment == label.NEGATIVE:
                    negative_tweets += 1
                elif tweet_sentiment == label.NEUTRAL:
                    neutral_tweets += 1
                else:
                    positive_tweets += 1

            # Ignore neutral tweets
            neutral_tweets = 0
            word_sentiment = utilities.get_sentiment_by_scores([negative_tweets, neutral_tweets, positive_tweets])
            result[word] = word_sentiment

        return result
