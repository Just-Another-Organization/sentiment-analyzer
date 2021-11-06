import torch

from utils.logger import Logger
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax
import numpy as np


class SentimentAnalyzer:
    def __init__(self):
        self.logger = Logger('SentimentAnalyzer')

        TASK = 'sentiment'
        MODEL = 'cardiffnlp/twitter-roberta-base-' + TASK

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        # Enable to save the model
        # self.model.save_pretrained(MODEL)

    # Preprocess text (username and link placeholders)
    def preprocess(self, text):
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def analyze_sentiment(self, text):
        text = self.preprocess(text)
        encoded_input = self.tokenizer(text, return_tensors='pt', max_length=490) # TODO: check this value
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        max_rank = max(scores)
        sentiment_index = np.where(scores == max_rank)[0]

        sentiment = ''
        if sentiment_index == 0:
            sentiment = 'negative'
        elif sentiment_index == 1:
            sentiment = 'neutral'
        elif sentiment_index == 2:
            sentiment = 'positive'

        return {
            'negative': scores[0],
            'neutral': scores[1],
            'positive': scores[2],
            'sentiment': sentiment
        }

    def test(self):
        text = """
        I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy.
        """
        # text = "Good night 😊"
        self.logger.info('Testing')
        scores = self.analyze_sentiment(text)
        self.logger.info(scores)

        return scores

    def analyze_keywords(self, keywords):
        result = {}
        for word in keywords:
            result[word] = word  # TODO

        return result



