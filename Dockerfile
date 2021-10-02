FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN python -m nltk.downloader vader_lexicon

COPY ./app .

EXPOSE 80

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
