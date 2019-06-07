import os
from invoke import task
from django.conf import settings

from witch import slackbot
from witch.tasks import utils

DOCKER_MACHINE_ENV = {
    'DOCKER_TLS_VERIFY': '1',
    'DOCKER_HOST': f'tcp://{settings.DOCKER_MACHINE_HOST}:2376',
    'DOCKER_CERT_PATH': settings.DOCKER_CERT_PATH,
    'DOCKER_MACHINE_NAME': settings.DOCKER_MACHINE_HOST
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


@task(pre=[utils.collect_static, utils.issue_certs])
def deploy(ctx):
    ctx.run(f'ssh {settings.DOCKER_MACHINE_USER}@{settings.DOCKER_MACHINE_HOST} -C "sudo docker image prune -a -f"')
    ctx.run(
        'docker-compose -f docker-compose.prod.yml up -d --build --remove-orphans',
        env=DOCKER_MACHINE_ENV
    )
    utils.print_task_done()
    slackbot.send('Deploy ended :satellite_antenna:')
