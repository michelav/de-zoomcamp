FROM python:3.9.1

RUN pip install sqlalchemy psycopg2 psycopg2-binary

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]