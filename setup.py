#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from gaft import __version__ as version

maintainer = 'Shao-Zheng-Jiang'
maintainer_email = 'shaozhengjiang@gmail.com'
author = maintainer
author_email = maintainer_email
description = "A Genetic Algorithm Framework in Python"
long_description = '''
====
gaft
====

A Genetic Algorithm Framework in PyThon

.. image:: https://travis-ci.org/PytLab/gaft.svg?branch=master
    :target: https://travis-ci.org/PytLab/gaft
    :alt: Build Status

.. image:: https://img.shields.io/badge/python-3.5, 2.7-green.svg
    :target: https://www.python.org/downloads/release/python-351/
    :alt: platform

.. image:: https://img.shields.io/badge/pypi-v0.1.1-blue.svg
    :target: https://pypi.python.org/pypi/gaft/
    :alt: versions


Introduction
------------

**gaft** is a Python Framework for genetic algorithm computation. It provide built-in genetic operators for genetic algorithm optimization and plugin interfaces for users to define your own genetic operators and on-the-fly analysis for algorithm testing.

Installation:
-------------

1. Via pip (not uploaded to PyPi yet):

    pip install gaft

2. From source:

    python setup.py install

'''
install_requires = []

license = 'LICENSE'

name = 'gaft'
packages = [
    'gaft',
]
platforms = ['linux', 'windows', 'macos']
url = 'https://github.com/PytLab/gaft'
download_url = 'https://github.com/PytLab/gaft/releases'

classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

setup(author=author,
      author_email=author_email,
      description=description,
      license=license,
      long_description=long_description,
      install_requires=install_requires,
      maintainer=maintainer,
      name=name,
      packages=find_packages(),
      platforms=platforms,
      url=url,
      download_url=download_url,
      version=version)

