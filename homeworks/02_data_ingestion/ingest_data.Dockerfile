FROM python:3.9.1

RUN pip install sqlalchemy psycopg2 psycopg2-binary pandas

WORKDIR /app
COPY dags/ingest_data.py ingest_data.py