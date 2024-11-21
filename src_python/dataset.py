import boto3
import os
from botocore import UNSIGNED
from botocore.config import Config

def main():
    bucket_name = 'softwareheritage'
    s3_folder = 'graph/2021-03-23-popular-3k-python/orc/'
    local_dir = r'C:\Users\rfon2\Documents\University\Fall2024\ECSE428\Dataset'

    download_s3_folder(bucket_name, s3_folder, local_dir)

def download_s3_folder(bucket_name, s3_folder, local_dir=None):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_folder):


        print("Downloading files from page", page)

        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('/'):
                continue
            local_file_path = key if local_dir is None else f"{local_dir}/{key[len(s3_folder):]}"
            local_file_dir = os.path.dirname(local_file_path)
            if not os.path.exists(local_file_dir):
                os.makedirs(local_file_dir)
            s3.download_file(bucket_name, key, local_file_path)

if __name__ == '__main__':
    main()