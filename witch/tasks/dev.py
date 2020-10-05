from invoke import task

from .utils import print_task_done

DOCKER_MACHINE_ENV = {
    'DOCKER_TLS_VERIFY': '',
    'DOCKER_HOST': '',
    'DOCKER_CERT_PATH': '',
    'DOCKER_MACHINE_NAME': ''
}

_DOCKER_COMPOSE_COMMAND = 'docker-compose -f ./docker/docker-compose.dev.yml'


@task
def start_db(ctx):
    ctx.run(
        '{} up -d --build --remove-orphans'.format(_DOCKER_COMPOSE_COMMAND),
        env=DOCKER_MACHINE_ENV
    )
    print_task_done()
