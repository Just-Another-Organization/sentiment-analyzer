from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Query

from services.sentiment_analyzer import SentimentAnalyzer
from services.trainer import Trainer
from services.twitter_connector import Twitter
from utils.list_string_flattening_middleware import QueryStringFlatteningMiddleware
from utils.logger import Logger

load_dotenv()

# Doc: http://127.0.0.1:8000/redoc
app = FastAPI(
    title="JASA",
    description="JASA - Just Another Sentiment Analyzer",
    version="0.1",
)

app.add_middleware(QueryStringFlatteningMiddleware)
logger = Logger('Main')
logger.info('Starting')

analyzer = SentimentAnalyzer()
twitter = Twitter()
trainer = Trainer()
trainer.test()

@app.get("/healthcheck")
def healthcheck():
    return {"Status": "Alive"}


@app.get("/sentiment-test")
def sentiment_test():
    return analyzer.test()


@app.get("/analyze-keywords")
def analyze_keywords(keywords: List[str] = Query(None)):

    result = analyzer.analyze_keywords(keywords)
    if keywords is not None:
        return {'result': result}
    else:
        return {"Error": "no keyword specified"}
