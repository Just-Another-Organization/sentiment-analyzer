import utils.constants as label
import utils.utilities as utilities
from models.TweetModel import TweetModel
from services.sentiment_analyzer import SentimentAnalyzer
from services.twitter import Twitter
from utils.logger import Logger


class Core:

    def __init__(self):
        self.logger = Logger('Core')
        self.analyzer = SentimentAnalyzer()
        self.twitter = Twitter()

    def test(self):
        self.twitter.test()

    def analyze_content_sentiment(self, content: TweetModel) -> tuple[str, int]:
        intensity = 1
        intensity += content.retweet_count + content.reply_count + content.favorite_count + content.quote_count
        text = content.text
        content_sentiment = self.analyzer.analyze_sentiment(text)
        return content_sentiment, intensity

    def analyze_keywords(self, keywords: list[str], ignore_neutral: bool = False, interval: str = None) \
            -> list[dict[str, str]]:
        results = []
        start_time = None
        end_time = None
        recent_mode = False

        if interval is not None:
            recent_mode = True
            start_time, end_time = utilities.get_interval(interval)

        for word in keywords:
            if recent_mode:
                self.logger.info('Searching recent tweets')
                contents = self.twitter.search_recent_tweets(keyword=word, start_time=start_time, end_time=end_time)
            else:
                self.logger.info('Searching popular tweets')
                contents = self.twitter.search_popular_tweets(keyword=word)

            negative_tweets = 0
            neutral_tweets = 0
            positive_tweets = 0

            if not contents:
                word_sentiment = 'NO_DATA_AVAILABLE'
                intensity = 0
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
                scores = [negative_tweets, neutral_tweets, positive_tweets]
                word_sentiment = utilities.get_sentiment_by_scores(scores)
                intensity = sum(scores)
            results.append({
                'keyword': word,
                'sentiment': word_sentiment,
                'intensity': intensity
            })

        return results
