from scipy.special import softmax
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

import utils.utilities as utilities
from utils.logger import Logger


class SentimentAnalyzer:
    TASK = 'sentiment'
    MODEL = 'cardiffnlp/twitter-roberta-base-' + TASK

    def __init__(self):
        self.logger = Logger('SentimentAnalyzer')
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL)
        # Enable to save the model
        # self.model.save_pretrained(MODEL)

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
        encoded_input = self.tokenizer(text, return_tensors='pt', max_length=512,
                                       truncation=True)  # TODO: check this value
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        sentiment = utilities.get_sentiment_by_scores(scores.tolist())

        return {
            'negative': scores[0],
            'neutral': scores[1],
            'positive': scores[2],
            'sentiment': sentiment
        }


