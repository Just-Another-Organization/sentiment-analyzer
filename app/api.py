from typing import List, Optional

from fastapi import APIRouter
from fastapi import Query
from starlette.requests import Request
from starlette.responses import Response

from services.core import Core
from utils.logger import Logger
from utils.requestlimiter import RequestLimiter

router = APIRouter()
core = Core()
logger = Logger('Api')
limiter = RequestLimiter.instance().limiter


@router.get("/healthcheck")
def healthcheck():
    return {"Status": "Alive"}


# @router.get("/test", include_in_schema=False)
# def sentiment_test():
#     return core.test()


# @router.get("/test-dataset")
# def sentiment_test():
#     return core.test_dataset()


@router.get("/analyze-keywords")
@limiter.limit("1/minute")
def analyze_keywords(request: Request, response: Response, keywords: List[str] = Query(None),
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
