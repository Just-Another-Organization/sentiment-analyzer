from fastapi import FastAPI
from textblob import TextBlob

# Doc: http://127.0.0.1:8000/redoc
app = FastAPI()

@app.get("/healthcheck")
def read_root():
    return {"Status": "Alive"}


@app.get("/sentiment-test")
def read_root():
    text = "I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy."

    blob = TextBlob(text)

    return {
        'Polarity:': blob.sentiment_assessments.polarity,
        'Sujectivity:': blob.sentiment_assessments. subjectivity,
        'Assessments:': blob.sentiment_assessments.assessments
    }
