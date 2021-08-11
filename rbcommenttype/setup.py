#!/usr/bin/env python

from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup

from rbcommenttype import get_package_version


with open('README.rst', 'r') as fp:
    long_description = fp.read()


setup(
    name='rbcommenttype',
    version=get_package_version(),
    description='Comment type categorization for Review Board',
    long_description=long_description,
    url='https://www.reviewboard.org/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=['rbcommenttype'],
    entry_points={
        'reviewboard.extensions': [
            'rbcommenttype = rbcommenttype.extension:CommentTypeExtension',
        ]
    },
    package_data={
        'rbcommenttype': [
            'templates/*.html',
            'templates/*.txt',
        ],
    },
    python_requires=(
        '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*'
        '!=3.5.*'
    ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Review Board',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Software Development :: Quality Assurance',
    ]
)
