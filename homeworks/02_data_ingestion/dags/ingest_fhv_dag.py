# pylint: disable=missing-function-docstring, missing-module-docstring

import os
from datetime import datetime
from airflow.decorators import dag
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from docker.types import Mount

AIRFLOW_DATA = os.environ.get('AIRFLOW_DATA', '/opt/airflow/data')
HOST_DIR = os.environ.get('HOST_DIR')
LOCAL_STORAGE = os.environ.get('LOCAL_STORAGE')
DB_USER = os.environ.get('LPG_USER')
DB_PASS = os.environ.get('LPG_PASS')
DB_PORT = '5432'
DB_NAME = os.environ.get('LPG_DB')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
MONTH = '{{ macros.ds_format(ds, \"%Y-%m-%d\", \"%Y-%m\") }}'

URL = f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{MONTH}.csv'
FILE_NAME = f"fhv_{MONTH}"
CSV_FILE = f'{AIRFLOW_DATA}/{FILE_NAME}.csv'
PARQUET_FILE = f'{AIRFLOW_DATA}/{FILE_NAME}.parquet'


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

@dag(default_args=default_args,
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2019, 12, 31),
    description='DAG that loads FHV data into GCS Bucket',
    schedule_interval='0 8 2 1-12 *',
    tags=['dezoomcamp', 'homework', 'w2', 'gcs'])
def ingest_fhv_gcs_dag():

    download_fhv_data = BashOperator(
        task_id='download_fhv_data',
        bash_command=f'curl -sSLf {URL} -o {CSV_FILE}',
    )

    t_parquet = DockerOperator(
        auto_remove=False,
        docker_url="tcp://docker-proxy:2375",
        image="elt_gcs",
        network_mode="airflow-net",
        mounts=[
                Mount(source=f'{HOST_DIR}/{LOCAL_STORAGE}', target=f'{AIRFLOW_DATA}', type='bind')
        ],
        command=[
            "python3",
            "elt_gcs.py",
            "--source",
            f"{CSV_FILE}",
            "parquet"
        ],
        task_id="parquet_fhv_data",
        mount_tmp_dir= False,
        container_name=f"TASK__PARQUET_FHV_DATA_{MONTH}",
        do_xcom_push=True
    )

    t_transfer = DockerOperator(
        auto_remove=False,
        docker_url="tcp://docker-proxy:2375",
        image="elt_gcs",
        network_mode="airflow-net",
        mounts=[
                Mount(source=f'{HOST_DIR}/{LOCAL_STORAGE}', target=f'{AIRFLOW_DATA}', type='bind')
        ],
        command=[
            "python3",
            "elt_gcs.py",
            "--source",
            f"{PARQUET_FILE}",
            "--dest",
            f"{BUCKET_NAME}",
            "transfer"
        ],
        task_id="transfer_parquet_fhv_data",
        mount_tmp_dir= False,
        container_name=f"TASK__TRANSFER_FHV_DATA_{MONTH}",
        do_xcom_push=True
    )

    download_fhv_data >> t_parquet >> t_transfer # pylint: disable=W0104

FHV_DAG = ingest_fhv_gcs_dag()
