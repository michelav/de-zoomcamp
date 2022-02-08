FROM python:3.9.1

RUN pip install pyarrow google-cloud-storage google-cloud-bigquery

WORKDIR /app
COPY dags/elt_gcs.py elt_gcs.py