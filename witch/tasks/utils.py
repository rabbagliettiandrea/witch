import os
from django.conf import settings

from invoke import task
from termcolor import colored

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


@task
def collect_static(ctx):
    print_info('Running collectstatic')
    ctx.run(
        'pipenv run python manage.py collectstatic --clear --noinput --verbosity 0',
        env={'DJANGO_SERVE_STATIC': '0'}
    )
    print_task_done()
