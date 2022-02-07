import argparse
import pandas as pd
from sqlalchemy import create_engine

def create_taxi_table(user, passwd, host, port, db_name, table_name, csv_file):
    df = pd.read_csv(csv_file, nrows=100)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    engine = create_engine(f'postgresql://{user}:{passwd}@{host}:{port}/{db_name}')
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f'Table {table_name} created.')

def csv_2_sql(user, passwd, host, port, db_name, table_name, csv_file):
    # csv_file = f'{AIRFLOW_DATA}/taxi_data_{MONTH}'
    # table_name = f'taxi_data_{MONTH}'
    # df = pd.read_csv(csv_file, nrows=5)
    # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    # engine = create_engine(f'postgresql://{user}:{passwd}@{host}:{port}/{db_name}')
    # df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    with open(csv_file, 'r', encoding='utf8') as file:
        conn = create_engine(f'postgresql://{user}:{passwd}@{host}:{port}/{db_name}').raw_connection()
        cursor = conn.cursor()
        cmd = f"COPY \"{table_name}\" FROM STDIN WITH (FORMAT CSV, HEADER)"
        cursor.copy_expert(cmd, file)
        conn.commit()
 
    print(f'NY Taxi data from file {csv_file} inserted.')

def load_taxi_data(params):
    create_taxi_table(params.user, params.password, params.host, params.port, params.db, params.tablename, params.csvfile)
    csv_2_sql(params.user, params.password, params.host, params.port, params.db, params.tablename, params.csvfile)

def load_fhv_data(params):
    print('load_fhv_data tbd')

dest = {
    'taxi': load_taxi_data,
    'fvh': load_fhv_data
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres', default='dezoomcamp')
    parser.add_argument('--password', help='password for postgres', default='dezoomcamp')
    parser.add_argument('--host', help='host for postgres', required=True)
    parser.add_argument('--port', help='port for postgres', default=5433)
    parser.add_argument('--db', help='database name for postgres', default='ny_taxi_db')
    parser.add_argument('--tablename', help='name of the table where we will write the results to', required=True)
    parser.add_argument('--csvfile', help='the csv file name', required=True)
    parser.add_argument('dest', help='Destination for csv file', choices=['taxi', 'fvh'])
    
    args = parser.parse_args()
    func = dest[args.dest]
    func(args)
    