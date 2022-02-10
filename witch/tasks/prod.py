from invoke import task
from django.conf import settings
from witch.tasks import aws, utils
import paramiko

WITCH_HOST_NAMES = getattr(settings, 'WITCH_K8S_NODES', [])

WITCH_HOST_USER = getattr(settings, 'WITCH_SSH_USER', None)


def get_ssh_client():
    for host in WITCH_K8S_NODES:
        try:
            ssh_client = paramiko.client.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.remote_host = host
            ssh_client.connect(hostname=host, username=WITCH_SSH_USER)
            return ssh_client
        except:
            continue

    utils.print_error('No hosts available')
    utils.abort()


def get_pod_name(ssh_client, service):
    try:
        return ssh_client.exec_command(
            'kubectl get pods -l app={} -o jsonpath="{{.items[0].metadata.name}}"'.format(service)
        )[1].read().decode('utf-8').strip()
    except:
        utils.print_error('Pod name not found')
        utils.abort()


@task
def exec(ctx, service='django', command='bash'):
    if WITCH_SSH_USER is None:
        utils.print_error('WITCH_SSH_USER setting not found.')
        utils.abort()

    ssh_client = get_ssh_client()
    pod_name = get_pod_name(ssh_client, service)
    ctx.run(
        'ssh -t {}@{} -C "kubectl exec -it {} -- {}"'.format(
            WITCH_SSH_USER,
            ssh_client.remote_host,
            pod_name,
            command
        ),
        pty=True
    )


@task
def shell(ctx, service='django'):
    return exec(ctx, service, command='python manage.py shell')
