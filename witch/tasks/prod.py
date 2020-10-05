from invoke import task
from django.conf import settings

from witch import slackbot
from witch.tasks import aws, utils

import functools

from time import sleep

WITCH_DOCKER_MACHINE = getattr(settings, 'WITCH_DOCKER_MACHINE', None)

if WITCH_DOCKER_MACHINE:
    DOCKER_MACHINE_ENV = {
        'DOCKER_TLS_VERIFY': '1',
        'DOCKER_HOST': 'tcp://{}:2376'.format(WITCH_DOCKER_MACHINE['host']),
        'DOCKER_CERT_PATH': WITCH_DOCKER_MACHINE['cert_path'],
        'DOCKER_MACHINE_NAME': WITCH_DOCKER_MACHINE['name']
    }

_DOCKER_COMPOSE_COMMAND = 'docker-compose -f ./docker/docker-compose.prod.yml'


@task
def logs(ctx, follow=False):
    ctx.run(
        '{} logs {}'.format(_DOCKER_COMPOSE_COMMAND, '-f' if follow else ''),
        env=DOCKER_MACHINE_ENV
    )


def start_service(ctx, service, rebuild=False):
    return ctx.run(
        '{} up -d {} --remove-orphans {}'.format(_DOCKER_COMPOSE_COMMAND, '--build' if rebuild else '', service),
        env=DOCKER_MACHINE_ENV
    )


def check_service(ctx, service):
    return ctx.run(
        '{} run --use-aliases nginx curl {}:8000 --head'.format(_DOCKER_COMPOSE_COMMAND, service),
        env=DOCKER_MACHINE_ENV, pty=True, warn=True, hide=True
    )


@task
def deploy(ctx):
    with aws.download_secrets(ctx):
        utils.migrate(ctx)
        ctx.run('ssh {}@{} -C "sudo docker image prune -a -f"'.format(
            settings.WITCH_DOCKER_MACHINE['user'],
            settings.WITCH_DOCKER_MACHINE['host']
        ))
        start_service(ctx, 'nginx', rebuild=True)
        start_service(ctx, 'django-blue', rebuild=True)
        utils.print_info('Sleeping waiting for "django-blue"')
        while not check_service(ctx, 'django-blue').ok:
            sleep(0.1)
        start_service(ctx, 'django-green')
        start_service(ctx, 'worker')
        start_service(ctx, 'beat')
    utils.print_task_done()
    slackbot.send('Deploy *ended* :satellite_antenna:')


@task
def exec(ctx, service='django-green', command='bash'):
    ctx.run(
        '{} exec {} {}'.format(_DOCKER_COMPOSE_COMMAND, service, command),
        env=DOCKER_MACHINE_ENV,
        pty=True
    )


@task
def shell(ctx, service='django-green'):
    return exec(ctx, service, command='python manage.py shell')
