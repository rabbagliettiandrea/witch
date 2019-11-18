import os

from django.conf import settings

from invoke import task
from invoke.exceptions import Failure
from termcolor import colored

import boto3
from contextlib import contextmanager, nullcontext

from witch import PROJECT_NAME


def _print_colored(msg, color):
    print(colored(f'\n-- {msg} --\n', color))


def print_task_done():
    _print_colored('TASK DONE', 'green')


def print_info(msg):
    _print_colored(msg, 'blue')


def print_success(msg):
    _print_colored(msg, 'green')


def print_warning(msg):
    _print_colored(msg, 'yellow')


def print_error(msg):
    _print_colored(msg, 'red')


def abort():
    raise Failure


@contextmanager
def aws_secrets(ctx):
    if hasattr(settings, 'WITCH_AWS_SECRET'):
        FILENAME = '.env.prod'
        session = boto3.session.Session(profile_name=settings.WITCH_AWS_SECRET['profile'])
        client = session.client(service_name='secretsmanager',  region_name=settings.WITCH_AWS_SECRET['region'])
        get_secret_value_response = client.get_secret_value(SecretId=settings.WITCH_AWS_SECRET['name'])
        secrets = get_secret_value_response['SecretString']
        if not secrets:
            print_error('AWS Data secrets empty')
            abort()
        with open(FILENAME, 'w') as fd:
            fd.write(secrets + '\n')
        yield
        os.remove(FILENAME)
    else:
        yield
        

@task
def collect_static(ctx):
    print_info('Running collectstatic')
    ctx.run(
        'python manage.py collectstatic --clear --noinput --verbosity 0',
        env={'DEBUG': '0'}
    )
    print_task_done()
    

@task
def migrate(ctx):
    print_info('Running migrate')
    ctx.run('python manage.py migrate')
    print_task_done()
