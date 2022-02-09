from invoke import task

from .utils import print_task_done

@task
def start_db(ctx):
    ctx.run('docker-compose --env-file ./.env up -d --build --remove-orphans')
    print_task_done()
