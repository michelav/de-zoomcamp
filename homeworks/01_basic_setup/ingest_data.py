#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from sqlalchemy import create_engine
from time import time


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    filename = params.filename

    t_start = time()
    
    with open(f'data/{filename}', 'r') as f:
        conn = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}').raw_connection()
        cursor = conn.cursor()
        cmd = f'COPY {table_name} FROM STDIN WITH (FORMAT CSV, HEADER)'
        cursor.copy_expert(cmd, f)
        conn.commit()
    
    t_end = time()
    print('Data inserted took %.3f second' % (t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres', default=5432)
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--filename', help='the csv file name')

    args = parser.parse_args()

    main(args)