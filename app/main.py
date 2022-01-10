from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Query

from services.core import Core
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

core = Core()


@app.get("/healthcheck")
def healthcheck():
    return {"Status": "Alive"}


@app.get("/sentiment-test")
def sentiment_test():
    return core.test()


@app.get("/sentiment-test-dataset")
def sentiment_test():
    return core.test_dataset()


@app.get("/analyze-keywords")
def analyze_keywords(keywords: List[str] = Query(None)):
    result = core.analyze_keywords(keywords)
    if keywords is not None:
        return {'result': result}
    else:
        return {"Error": "no keyword specified"}
