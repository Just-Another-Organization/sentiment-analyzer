from fastapi import APIRouter
from typing import List, Optional
from fastapi import Query
from services.core import Core
from utils.logger import Logger


router = APIRouter()
core = Core()
logger = Logger('Api')


@router.get("/healthcheck")
def healthcheck():
    return {"Status": "Alive"}


@router.get("/test")
def sentiment_test():
    return core.test()


@router.get("/test-dataset")
def sentiment_test():
    return core.test_dataset()


@router.get("/analyze-keywords")
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
