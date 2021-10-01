from textblob import TextBlob


class SentimentAnalyzer:
    def __init__(self):
        self.test()

    def check_sentiment(self, text):
        blob = TextBlob(text)
        return {
            'polarity:': blob.sentiment_assessments.polarity,
            'subjectivity:': blob.sentiment_assessments.subjectivity,
            'assessments:': blob.sentiment_assessments.assessments
        }

    def test(self):
        text = """
        I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy.
        """
        return self.check_sentiment(text)
