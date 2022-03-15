import os

from transformers import pipeline

import utils.utilities as utilities
from utils.logger import Logger


class SentimentAnalyzer:
    CLASSIFIER_NAME = os.getenv('CLASSIFIER_NAME', 'cardiffnlp/twitter-roberta-base-')
    CLASSIFIER_TASK = os.getenv('CLASSIFIER_TASK', 'sentiment')
    CLASSIFIER_TYPE = os.getenv('CLASSIFIER_TYPE', 'sentiment-analysis')

    MODEL = CLASSIFIER_NAME + CLASSIFIER_TASK

    def __init__(self):
        self.logger = Logger('SentimentAnalyzer')
        self.classifier = pipeline(self.CLASSIFIER_TYPE, model=self.MODEL)

    @staticmethod
    # Preprocess text (username and link placeholders)
    def preprocess(text):
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def analyze_sentiment(self, text):
        text = SentimentAnalyzer.preprocess(text)
        scores = self.classifier(text)
        sentiment = utilities.get_sentiment_by_label(scores[0]['label'])
        return sentiment
