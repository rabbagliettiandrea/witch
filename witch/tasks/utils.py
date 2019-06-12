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


@task
def issue_certs(ctx):
    if getattr(settings, 'WITCH_CERTBOT', {}):
        print_info('Running certbot')
        ctx.run(
            'certbot certonly '
            '-n --agree-tos --email {certbot_email} '
            '--config-dir {config_dir} --logs-dir {logs_dir} --work-dir {work_dir} --max-log-backups 0 '
            '--dns-cloudflare --dns-cloudflare-credentials {cloudflare_ini_path} '
            '--expand --cert-name {cert_name} '
            '{certbot_domains}'.format(
                certbot_email=settings.WITCH_CERTBOT['email'],
                config_dir=os.path.join(settings.WITCH_CERTBOT['base_dir'], 'config'),
                logs_dir=os.path.join(settings.WITCH_CERTBOT['base_dir'], 'logs'),
                work_dir=os.path.join(settings.WITCH_CERTBOT['base_dir'], 'work'),
                cloudflare_ini_path=os.path.join(settings.WITCH_CERTBOT['base_dir'], 'cloudflare.ini'),
                certbot_domains='-d {}'.format(' -d '.join(settings.WITCH_CERTBOT['domains'])),
                cert_name=PROJECT_NAME
            )
        )
    else:
        print_info('Skipping certbot')
    print_task_done()
