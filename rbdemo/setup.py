#!/usr/bin/env python

from reviewboard.extensions.packaging import setup
from setuptools import find_packages


PACKAGE = 'rbdemo'
VERSION = '2.0'

setup(
    name=PACKAGE,
    version=VERSION,
    description='Handles the demo management for demo.reviewboard.org',
    url='https://www.beanbaginc.com/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=find_packages(),
    python_requires='>=3.7',
    entry_points={
        'reviewboard.extensions': [
            'rbdemo = rbdemo.extension:DemoExtension',
        ],
    },
)
