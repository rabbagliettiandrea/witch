import os
from pathlib import Path
import sys

VERSION = '0.1.dev-1'

PROJECT_NAME = os.path.basename(os.path.normpath(Path().absolute()))

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{PROJECT_NAME}.settings')
