#!/usr/bin/env python

from reviewboard.extensions.packaging import setup
from setuptools import find_packages


setup(
    name='rbsentry',
    version='2.0',
    description='Error monitoring for Review Board using Sentry.io',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=find_packages(),
    install_requires=[
        'sentry-sdk',
    ],
    python_requires='>=3.7',
    entry_points={
        'reviewboard.extensions': [
            'rbsentry = rbsentry.extension:RbsentryExtension',
        ],
    },
    classifiers=[
        # For a full list of package classifiers, see
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers

        'Development Status :: 3 - Alpha',
        'Environment :: Web Framework',
        'Framework :: Review Board',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
