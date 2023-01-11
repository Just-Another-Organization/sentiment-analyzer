from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi import Query
from fastapi import status
from fastapi.openapi.models import APIKey
from starlette.requests import Request
from starlette.responses import Response

from services.core import Core
from utils.auth import Auth
from utils.logger import Logger
from utils.requestlimiter import RequestLimiter

router = APIRouter()
core = Core()
logger = Logger('Api')
request_limiter = RequestLimiter.instance()
limiter = request_limiter.limiter
auth = Auth()


@router.get("/health/check")
def healthcheck():
    return {"Status": "Alive"}


@router.get("/sentiment")
@limiter.limit("30/minute")
# request: Request param is needed due to @limiter
def analyze_keywords(request: Request, response: Response,
                     keywords: List[str] = Query(None),
                     ignore_neutral: Optional[bool] = False,
                     interval: Optional[str] = None,
                     combine: Optional[bool] = False,
                     api_key: APIKey = Depends(auth.api_key_auth)):
    if keywords is not None:
        if combine:
            keywords = [' '.join(keywords)]

        if request_limiter.api_limit_not_reached(len(keywords)):
            results = core.analyze_keywords(keywords, ignore_neutral, interval)
            response.status_code = status.HTTP_200_OK
            return results
        else:
            response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
            return {'Error': 'Limit reached'}
    else:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'Error': 'No keyword specified'}
