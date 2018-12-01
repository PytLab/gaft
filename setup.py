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
GAFT
====

A **G**\ enetic **A**\ lgorithm **F**\ ramework in py\ **T**\ hon

.. image:: https://travis-ci.org/PytLab/gaft.svg?branch=master
    :target: https://travis-ci.org/PytLab/gaft
    :alt: Build Status

.. image:: https://img.shields.io/codecov/c/github/PytLab/gaft/master.svg
    :target: https://codecov.io/gh/PytLab/gaft
    :alt: Codecov

.. image:: https://landscape.io/github/PytLab/gaft/master/landscape.svg?style=flat
    :target: https://landscape.io/github/PytLab/gaft/master
    :alt: Code Health

.. image:: https://img.shields.io/badge/python-3.5-green.svg
    :target: https://www.python.org/downloads/release/python-351/
    :alt: platform

.. image:: https://img.shields.io/badge/pypi-v0.5.7-blue.svg
    :target: https://pypi.python.org/pypi/gaft/
    :alt: versions

.. image:: https://readthedocs.org/projects/gaft/badge/?version=latest
    :target: https://gaft.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Introduction
------------

**GAFT** is a general Python Framework for genetic algorithm computation. It provides built-in genetic operators for target optimization and plugin interfaces for users to define your own genetic operators and on-the-fly analysis for algorithm testing.

**GAFT** is now accelerated using MPI parallelization interfaces. You can run it on your cluster in parallel with MPI environment.

Python Support
--------------

**GAFT** requires Python version 3.x (Python 2.x is not supported).

Installation
------------

1. Via pip::

    pip install gaft

2. From source::

    python setup.py install

If you want GAFT to run in MPI env, please install mpi4py explicitly::

    pip install mpi4py

See `INSTALL.md <https://github.com/PytLab/gaft/blob/master/INSTALL.md>`_ for more installation details.

Test
----

Run unit test::
    
    python setup.py test


'''

install_requires = [
]

license = 'LICENSE'

name = 'gaft'
platforms = ['linux', 'windows', 'macos']
url = 'https://github.com/PytLab/gaft'
download_url = 'https://github.com/PytLab/gaft/releases'

classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Utilities',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)'
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

test_suite = 'gaft.tests.test_all'

setup(
    author=author,
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
    version=version,
    test_suite=test_suite
)

