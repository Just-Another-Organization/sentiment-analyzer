from transformers import AutoModel, AutoTokenizer, pipeline, AutoModelForSequenceClassification

from utils.logger import Logger


class SentimentAnalyzer:
    def __init__(self):
        self.logger = Logger('SentimentAnalyzer')
        # model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
        model_name = "dbmdz/bert-base-cased-finetuned-conll03-english"
        # model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
        # model = AutoModelForSequenceClassification.from_pretrained(model_name)
        # tokenizer = AutoTokenizer.from_pretrained(model_name)
        # self.classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
        self.classifier = pipeline('sentiment-analysis')
        # self.logger.info(self.model)

        self.test()

    def analyze_sentiment(self, text):
        outputs = self.classifier(text)

        self.logger.info(outputs)

        return outputs

    def test(self):
        text = """
        I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy.
        """
        self.logger.info('Testing')
        output = self.analyze_sentiment(text)
        self.logger.info(output)
        return output

    def analyze_keywords(self, keywords):
        result = {}
        for word in keywords:
            result[word] = word  # TODO

        return result



