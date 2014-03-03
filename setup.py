#!/usr/bin/env python

import sys
from setuptools import setup, find_packages
from pda import __version__

with open('README.rst') as f:
    long_description = f.read()

extra_kwargs = {}
extra_kwargs['test_suite']       = 'test_pda'
extra_kwargs['install_requires'] = ['requests']

if sys.version_info < (2, 7):
    extra_kwargs['install_requires'].append('argparse>=1.2')
    extra_kwargs['setup_requires'] = ['unittest2']

setup(
name="pda",
version=__version__,
packages=find_packages(),
entry_points={
    'console_scripts': ['pda = pda.pda:main']
},
# scripts=['pda'],

# metadata
author="Henry Huang",
description='A command line tool managing all sorts of TODO lists',
long_description=long_description,
license='BSD',
url='https://github.com/keenhenry/pda',
platforms=['any'],
keywords='command line todo list TODO todolist',
classifiers=[ 'Development Status :: 3 - Alpha',
              'License :: OSI Approved :: BSD License',
              'Intended Audience :: End Users/Desktop',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: 2' ],
**extra_kwargs
)
