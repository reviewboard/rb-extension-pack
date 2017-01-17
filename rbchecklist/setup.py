#!/usr/bin/env python

from reviewboard.extensions.packaging import setup
from setuptools import find_packages

from rbchecklist import get_package_version


setup(
    name='rbchecklist',
    version=get_package_version(),
    description='Extension for Review Board which adds checklists for '
                'reviewers',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=find_packages(),
    entry_points={
        'reviewboard.extensions':
            'rbchecklist = rbchecklist.extension:Checklist',
    }
)
