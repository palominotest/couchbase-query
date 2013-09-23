#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
setup(
    name='python-couchbase-query',
    version='0.1b.dev',
    author='PalominoDB',
    author_email='oss@palominodb.com',
    py_modules=["query"],
    url="http://pypi.python.org/pypi/python-couchbase-query",
    license='GPLv2',
    description=' Connects to a couchbase instance and returns the contents of bucket given a key',
    install_requires=[
        'PyYAML>=3.10',
        'argparse>=1.2',
        'couchbase>=0.8',
        'logutils>=0.3',
    ],
    entry_points={
        'console_scripts': [
            'python-couchbase-query = query:main',
        ]
    }
)
