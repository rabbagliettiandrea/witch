from invoke import task

from . import utils

import shlex
import subprocess

from django.conf import settings
from django.core.management import BaseCommand, call_command

import django

django.setup()

COMMANDS = {
    'drop': '/usr/local/bin/dropdb --if-exists '
            '-h {restore_host} -U {db_user} {db_name}',
    'create': '/usr/local/bin/createdb '
              '-h {restore_host} -U {db_user} {db_name}',
    'dump': '/usr/local/bin/pg_dump --compress=9 --no-acl --format=c --no-owner '
            '-h {dump_host} -U {db_user_readonly} -d {db_name}',
    'restore': '/usr/local/bin/pg_restore '
               '-h {restore_host} -U {db_user} -d {db_name}'
}


def _get_params():
    local_host = settings.DATABASES['default']['HOST']
    if 'rds.amazonaws.com' in local_host:
        utils.print_error('[DISASTER PROTECTION] You\'re trying to restore to Amazon RDS')
        utils.abort()
    return {
        'restore_host': local_host,
        'restore_password': settings.DATABASES['default']['PASSWORD'],
        'db_user': settings.DATABASES['default']['USER'],
        'db_name': settings.DATABASES['default']['NAME'],
        'dump_host': settings.DATABASE_READONLY_HOST,
        'db_user_readonly': settings.DATABASE_READONLY_USER,
        'db_password_readonly': settings.DATABASE_READONLY_PASSWORD
    }


def _get_commands(params):
    return {k: shlex.split(v.format(**params)) for k, v in COMMANDS.items()}


@task
def download(ctx):
    params = _get_params()
    commands = _get_commands(params)
    try:
        utils.print_warning('Dropping DB')
        subprocess.run(
            args=commands['drop'], env={'PGPASSWORD': params['restore_password']},
            check=True,
            stdout=subprocess.PIPE
        )
        utils.print_warning('Creating DB')
        subprocess.run(
            args=commands['create'], env={'PGPASSWORD': params['restore_password']},
            check=True,
            stdout=subprocess.PIPE
        )
        utils.print_warning('Running pg_restore with pg_dump pipelining')
        p_dump = subprocess.Popen(
            args=commands['dump'], env={'PGPASSWORD': params['db_password_readonly']},
            stdout=subprocess.PIPE,
            bufsize=0
        )
        p_restore = subprocess.Popen(
            args=commands['restore'], env={'PGPASSWORD': params['restore_password']},
            stdin=p_dump.stdout, stdout=subprocess.PIPE,
            bufsize=0
        )
        p_restore.communicate()
        call_command('migrate', interactive=False)
        utils.print_success('Successfully synced DB with new migrations')
    except subprocess.CalledProcessError:
        utils.abort()
    utils.print_task_done()
