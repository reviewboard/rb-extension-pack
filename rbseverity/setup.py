#!/usr/bin/env python

from reviewboard.extensions.packaging import setup


PACKAGE = 'rbseverity'
VERSION = '0.1'

setup(
    name=PACKAGE,
    version=VERSION,
    description='Comment severity support for Review Board',
    url='http://www.beanbaginc.com/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=['rbseverity'],
    install_requires=[
        'ReviewBoard>=1.8alpha0.dev',
    ],
    entry_points={
        'reviewboard.extensions': [
            'rbseverity = rbseverity.extension:SeverityExtension',
        ],
    },
    package_data={
        'rbseverity': [
            'templates/rbseverity/*.html',
        ]
    },
)
