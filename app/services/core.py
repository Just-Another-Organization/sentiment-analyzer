import utils.costants as label
import utils.utilities as utilities
from models.Tweet import Tweet
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

    def analyze_content_sentiment(self, content: Tweet):
        intensity = 1
        intensity += content.retweet_count + content.reply_count + content.favorite_count + content.quote_count
        text = content.text
        content_sentiment = self.analyzer.analyze_sentiment(text)['sentiment']
        return content_sentiment, intensity

    def analyze_keywords(self, keywords, ignore_neutral=False, timeframe=None):
        result = {}
        start_time = None
        end_time = None
        recent_mode = False

        if timeframe is not None:
            recent_mode = True
            start_time, end_time = utilities.get_interval(timeframe)

        for word in keywords:
            if recent_mode:
                self.logger.info('Searching recent tweets')
                contents = self.twitter.search_recent(keyword=word, start_time=start_time, end_time=end_time)
            else:
                self.logger.info('Searching popular tweets')
                contents = self.twitter.search_popular_tweets(keyword=word)

            negative_tweets = 0
            neutral_tweets = 0
            positive_tweets = 0

            if not contents:
                result[word] = 'NO_DATA_AVAILABLE'
            else:
                for content in contents:
                    content_sentiment, intensity = self.analyze_content_sentiment(content)
                    if content_sentiment == label.NEGATIVE:
                        negative_tweets += intensity
                    elif content_sentiment == label.NEUTRAL:
                        neutral_tweets += intensity
                    else:
                        positive_tweets += intensity

                if ignore_neutral:
                    neutral_tweets = 0
                word_sentiment = utilities.get_sentiment_by_scores([negative_tweets, neutral_tweets, positive_tweets])
                result[word] = word_sentiment

        return result
