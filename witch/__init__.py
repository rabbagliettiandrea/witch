import os
from pathlib import Path
import sys
from dotenv import dotenv_values

__version__ = '0.1.dev-1'

config = dotenv_values('.env')

PROJECT_NAME = config.get('PROJECT_NAME') or os.path.basename(os.path.normpath(Path().absolute()))

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{PROJECT_NAME}.settings')
