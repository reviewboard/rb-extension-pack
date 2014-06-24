#!/usr/bin/env python

from reviewboard.extensions.packaging import setup

from rbnotefield import get_package_version


PACKAGE = 'rbnotefield'

setup(
    name=PACKAGE,
    version=get_package_version(),
    description='Adds a "Note to Reviewers" field for Review Board.',
    url='http://www.reviewboard.org/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=['rbnotefield'],
    entry_points={
        'reviewboard.extensions': [
            'rbnotefield = rbnotefield.extension:NoteFieldExtension',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Review Board',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
