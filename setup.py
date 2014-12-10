import os
from setuptools import setup

# http://bugs.python.org/issue8876#msg208792
# https://www.virtualbox.org/ticket/818
if os.path.abspath(__file__).split(os.path.sep)[1] == 'vagrant':
    del os.link

setup(
    name='challange-server',
    version = '0.1',
    description='Server app for challange',
    url='https://github.com/lhaze/challange-server',
    author='lhaze',
    author_email='lhaze@lhaze.name',
    package_dir = {'': 'challange'},
)