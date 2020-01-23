import os
import threading
from concurrent.futures.thread import ThreadPoolExecutor

from django.conf import settings

import boto3
from contextlib import contextmanager

from invoke import task

from witch.tasks import utils


@contextmanager
def dump_secrets(ctx):
    if hasattr(settings, 'WITCH_AWS_SECRET'):
        utils.print_info('Downloading AWS Secret')
        filename = '.env.prod'
        session = boto3.session.Session(profile_name=settings.WITCH_AWS_SECRET['profile'])
        client = session.client(service_name='secretsmanager', region_name=settings.WITCH_AWS_SECRET['region'])
        get_secret_value_response = client.get_secret_value(SecretId=settings.WITCH_AWS_SECRET['name'])
        secrets = get_secret_value_response['SecretString']
        if not secrets:
            utils.print_error('AWS Data secrets empty')
            utils.abort()
        with open(filename, 'w') as fd:
            fd.write(secrets + '\n')
        yield
        utils.print_info('Removing .env.prod file')
        os.remove(filename)
    else:
        utils.print_info('Skipping AWS Secret - no settings found')
        yield


@task
def s3download(ctx):
    def traverse_dirs(folder):
        def task(key):
            nonlocal pos
            download_to = os.path.join('.', key)
            with lock:
                if not os.path.exists(os.path.dirname(download_to)):
                    os.makedirs(os.path.dirname(download_to))
            if not os.path.exists(download_to):
                utils.print_info('Downloading {}: {}'.format(pos, key))
                client.download_file(bucket, key, download_to)
            with lock:
                pos += 1

        pos = 0
        paginator = client.get_paginator('list_objects')
        for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=folder):
            if result.get('CommonPrefixes') is not None:
                for subdir in result.get('CommonPrefixes'):
                    traverse_dirs(subdir.get('Prefix'))
            if result.get('Contents') is not None:
                with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
                    futures = executor.map(task, (d['Key'] for d in result.get('Contents')))
                    for _ in futures:
                        pass

    N_WORKERS = 32
    lock = threading.Lock()
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    client = session.client('s3')
    bucket = settings.AWS_STORAGE_BUCKET_NAME
    traverse_dirs('media')
    utils.print_success('Successfully downloaded AWS S3 media')
