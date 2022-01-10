from services.sentiment_analyzer import SentimentAnalyzer
from services.tester import Tester
from utils.logger import Logger


class Core:

    def __init__(self):
        self.logger = Logger('Core')
        self.analyzer = SentimentAnalyzer()
        self.tester = Tester(self.analyzer)

    def test(self):
        self.tester.test()

    def test_dataset(self):
        self.tester.test_dataset()

    def analyze_keywords(self, keywords):
        result = {}
        for word in keywords:
            result[word] = word  # TODO

        return result
