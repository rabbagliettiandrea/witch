import os
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from django.conf import settings
import boto3
from invoke import task
from witch.tasks import utils


@task
def s3download(ctx):
    def traverse_dirs(folder, lock=threading.Lock()):
        def task(key):
            download_to = os.path.join('.', key).replace(
                '/{}'.format(settings.AWS_LOCATION),
                '/{}'.format(os.path.basename(settings.MEDIA_ROOT))
            )
            with lock:
                if not os.path.exists(os.path.dirname(download_to)):
                    os.makedirs(os.path.dirname(download_to))
            if not os.path.exists(download_to):
                utils.print_info('Downloading {} -> {}'.format(key, download_to))
                client.download_file(bucket, key, download_to)
            else:
                utils.print_warning('Skipping {}'.format(key))

        paginator = client.get_paginator('list_objects')
        for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=folder):
            if result.get('CommonPrefixes') is not None:
                for subdir in result.get('CommonPrefixes'):
                    traverse_dirs(subdir.get('Prefix'), lock=lock)
            if result.get('Contents') is not None:
                with ThreadPoolExecutor(max_workers=32) as executor:
                    futures = executor.map(task, (d['Key'] for d in result.get('Contents')))
                    for _ in futures:
                        pass

    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    client = session.client('s3')
    bucket = settings.AWS_STORAGE_BUCKET_NAME
    traverse_dirs(settings.AWS_LOCATION)
    utils.print_success('Successfully downloaded AWS S3 media')

