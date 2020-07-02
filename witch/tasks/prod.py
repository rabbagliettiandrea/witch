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


@task
def ps(ctx):
    cmd = 'docker-compose -f docker-compose.prod.yml ps'
    ctx.run(cmd, env=DOCKER_MACHINE_ENV)


@task
def logs(ctx, follow=False):
    cmd = 'docker-compose -f docker-compose.prod.yml logs'
    ctx.run(
        '{} -f'.format(cmd) if follow else cmd,
        env=DOCKER_MACHINE_ENV
    )


def start_service(ctx, service):
    return ctx.run(
        'docker-compose -f docker-compose.prod.yml '
        'up -d --build --remove-orphans {}'.format(service),
        env=DOCKER_MACHINE_ENV
    )


def check_service(ctx, service):
    return ctx.run(
        'docker-compose -f docker-compose.prod.yml '
        'run --use-aliases nginx curl {}:8000 --head'.format(service),
        env=DOCKER_MACHINE_ENV, pty=True, warn=True, hide=True
    )


@task
def deploy(ctx):
    with aws.dump_secrets(ctx):
        utils.migrate(ctx)
        ctx.run('ssh {}@{} -C "sudo docker image prune -a -f"'.format(
            settings.WITCH_DOCKER_MACHINE['user'],
            settings.WITCH_DOCKER_MACHINE['host']
        ))
        start_service(ctx, 'nginx')
        start_service(ctx, 'django-blue')
        while not check_service(ctx, 'django-blue').ok:
            sleep(1)
            utils.print_info('Sleeping waiting for "django-blue"')
        start_service(ctx, 'django-green')
    utils.print_task_done()
    slackbot.send('Deploy *ended* :satellite_antenna:')


@task
def exec(ctx, service='django', command='bash'):
    cmd = 'docker-compose -f docker-compose.prod.yml exec {} {}'.format(service, command)
    ctx.run(cmd, env=DOCKER_MACHINE_ENV, pty=True)
