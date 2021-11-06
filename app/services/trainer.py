import pandas as pd
from datasets import load_dataset

from services.sentiment_analyzer import SentimentAnalyzer
from utils.logger import Logger


class Trainer:
    def __init__(self):
        self.logger = Logger('Trainer')
        self.analyzer = SentimentAnalyzer()

    def read_dataset(self):
        imdb_dataset = load_dataset('imdb', split='train')
        return pd.DataFrame(imdb_dataset.to_pandas())

    def test(self):
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
