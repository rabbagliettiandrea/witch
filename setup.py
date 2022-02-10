from setuptools import setup, find_packages

from witch import VERSION

setup(
    name='witch',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/rabbagliettiandrea/witch',
    install_requires=[
        'invoke==1.2.0',
        'termcolor==1.1.0',
        'boto3~=1.9',
        'python-dotenv==0.15.0',
        'paramiko'

    ],
    entry_points={
        'console_scripts': ['witch = witch.main:program.run']
    }
)
