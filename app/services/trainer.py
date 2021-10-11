import os.path

import pandas as pd

from services.sentiment_analyzer import SentimentAnalyzer
from utils.logger import Logger

dirname = os.path.dirname(__file__)
datasets_folder = os.path.join(dirname, "../datasets/")
dataset = os.path.join(datasets_folder, "IMDB Dataset.csv")


class Trainer:
    def __init__(self):
        self.logger = Logger('Trainer')
        self.analyzer = SentimentAnalyzer()
        self.test()

    def read_dataset(self):
        return pd.read_csv(dataset)

    def test(self):
        if os.path.isfile(dataset):
            df = self.read_dataset()
            correct = 0
            incorrect = 0
            for index, row in df.iterrows():
                if index % 1000 == 0:
                    self.logger.info(index)
                text = row[0]
                sentiment = row[1]
                sentiment_analysis = self.analyzer.analyze_sentiment(text)
                compound = sentiment_analysis['compound']
                positivity = sentiment_analysis['positive']
                negativity = sentiment_analysis['negative']
                if compound > 0 and positivity > negativity:
                    predicted_sentiment = 'positive'
                else:
                    predicted_sentiment = 'negative'
                if predicted_sentiment == sentiment:
                    correct += 1
                else:
                    incorrect += 1

            self.logger.info(correct)
            self.logger.info(incorrect)
        else:
            self.logger.info('No datasets available')
