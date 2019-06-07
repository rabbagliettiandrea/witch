import os
import subprocess
import shlex
from pathlib import Path
import sys

VERSION = '0.1.dev-{}'.format(
    subprocess.check_output(shlex.split('git rev-parse --short HEAD')).rstrip().decode()
)

PROJECT_NAME = os.path.basename(os.path.normpath(Path().absolute()))

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{PROJECT_NAME}.settings')