FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

RUN python -m textblob.download_corpora
RUN python -m spacy download en_core_web_sm

COPY ./app .

EXPOSE 80