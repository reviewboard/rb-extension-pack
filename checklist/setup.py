#!/usr/bin/env python

from reviewboard.extensions.packaging import setup


PACKAGE = "checklist"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Extension for Review Board which adds checklists for reviewers",
    author="Mary Elaine Malit",
    packages=["checklist"],
    entry_points={
        'reviewboard.extensions':
            '%s = checklist.extension:Checklist' % PACKAGE,
    },
    package_data={
        'checklist': [
            'templates/checklist/*.txt',
            'templates/checklist/*.html',
        ],
    }
)
