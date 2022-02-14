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

URL = 'https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'
FILE_NAME = 'taxi_zone_lookup.csv'
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
    schedule_interval='@once',
    tags=['dezoomcamp', 'homework', 'w2', 'gcs'])
def ingest_zone_gcs_dag():

    download_zone_data = BashOperator(
        task_id='download_zone_data',
        bash_command=f'curl -sSLf {URL} -o {CSV_FILE}',
    )

    t_parquet = DockerOperator(
        auto_remove=True,
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
        task_id="parquet_zone_data",
        mount_tmp_dir= False,
        container_name='TASK__PARQUET_ZONE_DATA',
        do_xcom_push=True
    )

    t_transfer = DockerOperator(
        auto_remove=True,
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
        task_id="transfer_parquet_zone_data",
        mount_tmp_dir= False,
        container_name='TASK__TRANSFER_ZONE_DATA',
        do_xcom_push=True
    )

    download_zone_data >> t_parquet >> t_transfer # pylint: disable=W0104

FHV_DAG = ingest_zone_gcs_dag()
