from invoke import task

from .utils import print_task_done

DOCKER_MACHINE_ENV = {
    'DOCKER_TLS_VERIFY': '',
    'DOCKER_HOST': '',
    'DOCKER_CERT_PATH': '',
    'DOCKER_MACHINE_NAME': ''
}


@task
def start_db(ctx):
    ctx.run(
        'docker-compose -f docker-compose.yml up -d --build --remove-orphans',
        env=DOCKER_MACHINE_ENV
    )
    print_task_done()
