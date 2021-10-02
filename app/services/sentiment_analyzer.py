from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    def __init__(self):
        # Initialize the VADER sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text):
        scores = self.analyzer.polarity_scores(text)
        result = dict()
        result['negative'] = scores['neg']
        result['neutral'] = scores['neu']
        result['positive'] = scores['pos']
        result['compound'] = scores['compound']

        return result

    def test(self):
        text = """
        I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy.
        """
        return self.analyze_sentiment(text)

    def analyze_keywords(self, keywords):
        result = {}
        for word in keywords:
            result[word] = word  # TODO

        return result

    def load_model(self):
        pass
