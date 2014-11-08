#!/usr/bin/env python
from reviewboard.extensions.packaging import setup

from rbslack import get_package_version


PACKAGE = 'rbslack'

setup(
    name=PACKAGE,
    version=get_package_version(),
    description='Review Board integration for slack.com',
    url='https://www.beanbaginc.com',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=['rbslack'],
    entry_points={
        'reviewboard.extensions':
            '%s = rbslack.extension:SlackExtension' % PACKAGE,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Review Board',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
