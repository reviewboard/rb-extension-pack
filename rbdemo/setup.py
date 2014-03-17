#!/usr/bin/env python

from reviewboard.extensions.packaging import setup
from setuptools import find_packages


PACKAGE = 'rbdemo'
VERSION = '0.1'

setup(
    name=PACKAGE,
    version=VERSION,
    description='Handles the demo management for demo.reviewboard.org',
    url='http://www.beanbaginc.com/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=find_packages(),
    entry_points={
        'reviewboard.extensions': [
            'rbdemo = rbdemo.extension:DemoExtension',
        ],
    },
)
