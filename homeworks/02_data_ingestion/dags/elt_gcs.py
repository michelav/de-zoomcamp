import logging
import argparse


from google.cloud import storage
import pyarrow.csv as pv
import pyarrow.parquet as pq

def to_parquet(params):
    """
    Convert CSV files to parquet
    """
    source = params.source
    if not source.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(source)
    pq.write_table(table, source.replace('.csv', '.parquet'))


# NOTE: takes 20 mins, at an upload speed of 800kbps.
# Faster if your internet has a better upload speed.
def upload_to_gcs(params):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(params.dest)

    blob = bucket.blob(params.name)
    blob.upload_from_filename(params.source)

route = {
    'parquet': to_parquet,
    'transfer': upload_to_gcs,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ELT CSV Data to GCS')

    parser.add_argument('--source', help='the csv file name', required=True)
    parser.add_argument('--dest', help='the bucket destination', required=False)
    parser.add_argument('--name', help='the object name', required=False)
    parser.add_argument('operation', help='Operation to be performed', choices=['parquet', 'transfer'])

    args = parser.parse_args()
    func = route[args.operation]
    func(args)
