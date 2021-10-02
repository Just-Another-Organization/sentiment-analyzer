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
        analyzer = SentimentAnalyzer()

    def read_dataset(self):
        return pd.read_csv(dataset)

    def train(self):
        df = self.read_dataset()
        self.logger.info(df)
