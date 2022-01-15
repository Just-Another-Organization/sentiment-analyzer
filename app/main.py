import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, FileResponse

import api
from utils.list_string_flattening_middleware import QueryStringFlatteningMiddleware

favicon_path = 'static/favicon.ico'
load_dotenv()

STATIC_FILES_PATH = "/engine"
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(",")

# Doc: http://127.0.0.1:80/redoc
app = FastAPI(
    title="JASA",
    description="JASA - Just Another Sentiment Analyzer",
    version="0.1",
)

app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_HOSTS)
app.add_middleware(QueryStringFlatteningMiddleware)
app.mount(STATIC_FILES_PATH, StaticFiles(directory="static", html=True), name="static")

app.include_router(
    api.router,
    prefix="/api",
    tags=["api"])


@app.get("/", include_in_schema=False)
async def redirect():
    response = RedirectResponse(url=STATIC_FILES_PATH)
    return response


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
