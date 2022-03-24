#!/usr/bin/env python

from reviewboard.extensions.packaging import setup

from rbseverity import get_package_version


PACKAGE = 'rbseverity'

setup(
    name=PACKAGE,
    version=get_package_version(),
    description='Comment severity fields for Review Board.',
    url='http://www.reviewboard.org/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=['rbseverity'],
    python_requires='>=3.7',
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
