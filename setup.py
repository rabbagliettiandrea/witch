from setuptools import setup, find_packages

from witch import VERSION

setup(
    name='witch',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/spesa-online/witch',
    install_requires=[
        'invoke==1.2.0',
        'slackclient~=2.0', 
        'termcolor==1.1.0',
        'boto3'
    ],
    entry_points={
        'console_scripts': ['witch = witch.main:program.run']
    }
)
