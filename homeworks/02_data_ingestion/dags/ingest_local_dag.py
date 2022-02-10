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
MONTH = '{{ macros.ds_format(ds, \"%Y-%m-%d\", \"%Y-%m\") }}'

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

@dag(default_args=default_args,
    start_date=datetime(2021, 1, 1),
    description='DAG that loads NY Taxi CSV data into a local Postgresql database',
    schedule_interval='0 8 2 1-3 *',
    tags=['dezoomcamp', 'homework', 'w2'])
def ingest_data_local_pg_dag():

    URL = f'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_{MONTH}.csv'
    OUTPUT_FILE = f'{AIRFLOW_DATA}/taxi_data_{MONTH}.csv'
    CONTAINER_NAME = f'_task__ingest_taxi_data_{MONTH}_'

    download_taxi_data = BashOperator(
        task_id='download_taxi_data',
        bash_command=f'curl -sSLf {URL} -o {OUTPUT_FILE}',
    )

    print('The URL is: ' + URL)
    print('The Output File is: ' + OUTPUT_FILE)
    print('The Month is: ' + MONTH)
    print('The Container Name is: ' + CONTAINER_NAME)

    t_load = DockerOperator(
        auto_remove=False,
        docker_url="tcp://docker-proxy:2375",
        image="ingest_data",
        network_mode="airflow-net",
        mounts=[
                Mount(source=f'{HOST_DIR}/{LOCAL_STORAGE}', target=f'{AIRFLOW_DATA}', type='bind')
        ],
        command=[
            "python3",
            "ingest_data.py",
            "--user",
            f"{DB_USER}",
            "--password",
            f"{DB_PASS}",
            "--host",
            "pgdb",
            "--port",
            f"{DB_PORT}",
            "--db",
            f"{DB_NAME}",
            "--tablename",
            f"taxi_data_{MONTH}",
            "--csvfile",
            f"{OUTPUT_FILE}",
            "taxi"
        ],
        task_id="ingest_taxi_data",
        mount_tmp_dir= False,
        container_name=f"TASK__INGEST_TAXI_DATA_{MONTH}",
        do_xcom_push=True
    )

    download_taxi_data >> t_load

dag = ingest_data_local_pg_dag()