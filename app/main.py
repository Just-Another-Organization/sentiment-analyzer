import api
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from utils.list_string_flattening_middleware import QueryStringFlatteningMiddleware

load_dotenv()

# Doc: http://127.0.0.1:80/redoc
app = FastAPI(
    title="JASA",
    description="JASA - Just Another Sentiment Analyzer",
    version="0.1",
)

app.add_middleware(QueryStringFlatteningMiddleware)
app.mount("/engine", StaticFiles(directory="static", html=True), name="static")

app.include_router(
    api.router,
    prefix="/api",
    tags=["api"])
