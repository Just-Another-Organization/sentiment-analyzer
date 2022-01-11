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

    def analyze_content_sentiment(self, content):
        text = str(content.text)
        content_sentiment = self.analyzer.analyze_sentiment(text)['sentiment']
        return content_sentiment

    def analyze_keywords(self, keywords, ignore_neutral=False, timeframe='1h'):
        result = {}
        start_time, end_time = utilities.get_interval(timeframe)
        for word in keywords:
            contents = self.twitter.search(keyword=word, limit=100, start_time=start_time, end_time=end_time)
            negative_tweets = 0
            neutral_tweets = 0
            positive_tweets = 0

            if not contents:
                result[word] = 'NO_DATA_AVAILABLE'
            else:
                for content in contents:
                    content_sentiment = self.analyze_content_sentiment(content)
                    if content_sentiment == label.NEGATIVE:
                        negative_tweets += 1
                    elif content_sentiment == label.NEUTRAL:
                        neutral_tweets += 1
                    else:
                        positive_tweets += 1

                if ignore_neutral:
                    neutral_tweets = 0
                word_sentiment = utilities.get_sentiment_by_scores([negative_tweets, neutral_tweets, positive_tweets])
                result[word] = word_sentiment

        return result
