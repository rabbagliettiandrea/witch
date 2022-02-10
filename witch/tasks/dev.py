from invoke import task

from .utils import print_task_done

@task
def start_services(ctx):
    ctx.run('docker-compose up -d --build --remove-orphans')
    print_task_done()
