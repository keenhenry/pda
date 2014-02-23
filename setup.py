#!/usr/bin/env python

from distutils.core import setup

long_description = open('README.rst').read()

setup(
name="pda",
author="Henry Huang",
packages=['listdb'],
description='A command line tool managing all sorts of TODO lists',
long_description=long_description,
license='BSD',
url='https://github.com/keenhenry/pda',
version="0.0.4",
platforms=['any'],
scripts=["pda"]
)
