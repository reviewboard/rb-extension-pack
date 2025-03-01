#!/usr/bin/env python3

from reviewboard.extensions.packaging import setup

from rbmotd import get_package_version


PACKAGE = 'rbmotd'

setup(
    name=PACKAGE,
    version=get_package_version(),
    description='Message of the Day support for Review Board',
    url='https://www.reviewboard.org/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=['rbmotd'],
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
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Review Board',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ]
)
