from fastapi import FastAPI
from services.sentiment_analyzer import SentimentAnalyzer

# Doc: http://127.0.0.1:8000/redoc
app = FastAPI()

analyzer = SentimentAnalyzer()


@app.get("/healthcheck")
def read_root():
    return {"Status": "Alive"}


@app.get("/sentiment-test")
def sentiment_test():
    return analyzer.test()
