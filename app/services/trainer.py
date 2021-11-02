from services.sentiment_analyzer import SentimentAnalyzer
from utils.logger import Logger
from datasets import load_dataset
import pandas as pd


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
            lab = labels[i]

            sentiment_analysis = self.analyzer.analyze_sentiment(text)

            print(sentiment_analysis)

            if lab == 1:
                sentiment = 'POSITIVE'
            else:
                sentiment = 'NEGATIVE'
            if sentiment == sentiment_analysis[0]['label']:
                correct += 1
            else:
                incorrect += 1

            if i % 100 == 0:
                self.logger.info('Index: ' + str(i))
                self.logger.info(correct)
                self.logger.info(incorrect)

        self.logger.info(correct)
        self.logger.info(incorrect)
