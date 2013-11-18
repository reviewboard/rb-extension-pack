#!/usr/bin/env python

from reviewboard.extensions.packaging import setup


PACKAGE = 'rbmotd'
VERSION = '0.1'

setup(
    name=PACKAGE,
    version=VERSION,
    description='Message of the Day support for Review Board',
    url='http://www.beanbaginc.com/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=['rbmotd'],
    install_requires=[
        'ReviewBoard>=2.0beta2.dev',
    ],
    entry_points={
        'reviewboard.extensions': [
            'rbmotd = rbmotd.extension:MotdExtension',
        ],
    },
    package_data={
        'rbmotd': [
            'templates/rbmotd/*.html',
        ]
    },
)
