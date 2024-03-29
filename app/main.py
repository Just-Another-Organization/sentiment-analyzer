import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

import api
from utils.list_string_flattening_middleware import QueryStringFlatteningMiddleware
from utils.requestlimiter import RequestLimiter

load_dotenv()
dirname = os.path.dirname(__file__)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(",")

# Doc: http://127.0.0.1:80/redoc
app = FastAPI(
    title="JASA",
    description="JASA - Just Another Sentiment Analyzer",
    version="0.1",
)
app.state.limiter = RequestLimiter.instance().limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_HOSTS)
app.add_middleware(QueryStringFlatteningMiddleware)

app.include_router(
    api.router,
    prefix="/api/v1",
    tags=["api"])
