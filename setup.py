import os
import re
import codecs
from setuptools import setup, find_packages

def read(package_name, file_name):
    filename = os.path.join(os.path.dirname(__file__), package_name, file_name)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(package_name, file_name):
    version_file = read(package_name, file_name)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')

setup(
    name='witch',
    version=find_version("witch", "__init__.py"),
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/rabbagliettiandrea/witch',
    install_requires=[
        'invoke==1.2.0',
        'termcolor==1.1.0',
        'boto3~=1.9',
        'python-dotenv==0.20.0'
    ],
    entry_points={
        'console_scripts': ['witch = witch.main:program.run']
    }
)
