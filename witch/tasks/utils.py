from invoke import task
from invoke.exceptions import Exit
from termcolor import colored
from datetime import datetime


def _print(msg, color):
    print(colored('\n-- [{:%H:%M:%S}] {} --\n'.format(datetime.now(), msg), color))


def print_task_done():
    _print('TASK DONE', 'green')


def print_info(msg):
    _print(msg, 'blue')


def print_success(msg):
    _print(msg, 'green')


def print_warning(msg):
    _print(msg, 'yellow')


def print_error(msg):
    _print(msg, 'red')


def abort():
    raise Exit(code=-1)


@task
def migrate(ctx):
    print_info('Running migrate')
    ctx.run('python manage.py migrate')
    print_task_done()
