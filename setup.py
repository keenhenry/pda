#!/usr/bin/env python

import sys
from setuptools import setup, find_packages
from pda import __version__

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()

extra_kwargs = {}
extra_kwargs['test_suite']       = 'test_pda'
extra_kwargs['setup_requires']   = ['mock']
extra_kwargs['install_requires'] = ['requests']

if sys.version_info < (2, 7):
    extra_kwargs['install_requires'].append('argparse>=1.2')

setup(
name="pda",
version=__version__,
packages=find_packages(),
entry_points={
    'console_scripts': ['pda = pda.control:main']
},
zip_safe=True,

# metadata
author="Henry Huang",
description='A command line todo list manager',
long_description=readme + '\n\n' + history,
license='BSD',
url='https://github.com/keenhenry/pda',
platforms=['any'],
keywords='command line todo list TODO todolist',
classifiers=[ 'Development Status :: 4 - Beta',
              'License :: OSI Approved :: BSD License',
              'Intended Audience :: Developers',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 2.6',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4'
              ],
**extra_kwargs
)
