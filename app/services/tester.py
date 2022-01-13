import pandas as pd
from datasets import load_dataset
from services.sentiment_analyzer import SentimentAnalyzer
from utils.logger import Logger


class Tester:
    def __init__(self, analyzer: SentimentAnalyzer):
        self.logger = Logger('Trainer')
        self.analyzer = analyzer

    @staticmethod
    def read_dataset():
        imdb_dataset = load_dataset('imdb', split='train')
        return pd.DataFrame(imdb_dataset.to_pandas())

    def test(self):
        self.logger.info('Testing')
        text = """
        I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy.
        """
        scores = self.analyzer.analyze_sentiment(text)
        self.logger.info(scores)
        return scores

    def test_dataset(self):
        df = self.read_dataset()
        correct = 0
        incorrect = 0

        texts = df['text'].to_list()
        labels = df['label'].to_list()

        elements = len(df)

        for i in range(elements):
            text = texts[i]
            label = labels[i]

            sentiment_analysis = self.analyzer.analyze_sentiment(text)

            if label == 1:
                sentiment = 'positive'
            else:
                sentiment = 'negative'

            negative_score = sentiment_analysis['negative']
            positive_score = sentiment_analysis['positive']
            if negative_score > positive_score:
                predicted_sentiment = 'negative'
            else:
                predicted_sentiment = 'positive'

            if sentiment == predicted_sentiment:
                correct += 1
            else:
                incorrect += 1

            if i % 100 == 0:
                self.logger.info('Index: ' + str(i))
                self.logger.info(correct)
                self.logger.info(incorrect)

        self.logger.info('Correct: ' + str(correct))
        self.logger.info('Incorrect: ' + str(incorrect))
