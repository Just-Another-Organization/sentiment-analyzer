from typing import List, Optional

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


@app.get("/test")
def sentiment_test():
    return core.test()


@app.get("/test-dataset")
def sentiment_test():
    return core.test_dataset()


@app.get("/analyze-keywords")
def analyze_keywords(keywords: List[str] = Query(None),
                     ignore_neutral: Optional[bool] = False,
                     timeframe: Optional[str] = None,
                     combine: Optional[bool] = False):
    if keywords is not None:
        if combine:
            keywords = [' '.join(keywords)]

        result = core.analyze_keywords(keywords, ignore_neutral, timeframe)
        return {'result': result}
    else:
        return {"Error": "no keyword specified"}
