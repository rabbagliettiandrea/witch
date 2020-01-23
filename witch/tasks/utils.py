from invoke import task
from invoke.exceptions import Exit
from termcolor import colored


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


def abort():
    raise Exit(code=-1)


@task
def collect_static(ctx):
    print_info('Running collectstatic')
    ctx.run(
        'python manage.py collectstatic --clear --noinput --verbosity 0',
        env={'DEBUG': '0'}
    )
    print_task_done()


@task
def migrate(ctx):
    print_info('Running migrate')
    ctx.run('python manage.py migrate')
    print_task_done()
