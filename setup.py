import os
from setuptools import setup

# distutils/hardlinks workaround:
# http://bugs.python.org/issue8876#msg208792
# https://www.virtualbox.org/ticket/818
if os.path.abspath(__file__).split(os.path.sep)[1] == 'vagrant':
    del os.link


setup(
    name='challenge-server',
    version='0.1',
    description='Server app for challenge',
    url='https://github.com/lhaze/challenge-server',
    author='lhaze',
    author_email='lhaze@lhaze.name',
    package_dir={'': 'challenge'},
    requires=[
        'dharma'
    ]
)
