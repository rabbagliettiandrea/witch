import random

from invoke import task
from django.conf import settings
from witch.tasks import aws, utils

WITCH_K8S_NODES = getattr(settings, 'WITCH_K8S_NODES', [])

WITCH_SSH_USER = getattr(settings, 'WITCH_SSH_USER', None)


@task
def exec(ctx, service='django', command='bash'):
    if WITCH_SSH_USER is None:
        utils.print_error('WITCH_SSH_USER setting not found.')
        utils.abort()

    for node in random.choices(WITCH_K8S_NODES):
        try:
            a = ctx.run(
                'ssh -t {}@{} -C "kubectl exec -it \$({}) -- {}"'.format(
                    WITCH_SSH_USER,
                    node,
                    "kubectl get pods -l app={} | grep 'Running' | sed 's/|/ /' | awk '{{print $1}}' | shuf -n 1".format(service),
                    command
                ),
                pty=True, warn=False
            )
            return
        except:
            continue

    utils.print_error('No nodes available')
    utils.abort()

@task
def shell(ctx, service='django'):
    return exec(ctx, service, command='python manage.py shell')
