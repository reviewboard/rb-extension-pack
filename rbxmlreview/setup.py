#!/usr/bin/env python
from setuptools import setup


PACKAGE = "rbxmlreview"
VERSION = "1.0"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Review Board extension for XML review UI and "
                "thumbnail support",
    author="Sampson Chen",
    packages=["rbxmlreview"],
    python_requires='>=3.7',
    entry_points={
        'reviewboard.extensions':
            '%s = rbxmlreview.extension:XMLReviewUIExtension'
            % PACKAGE,
    },
    package_data={
        'rbxmlreview': [
            'htdocs/css/*.css',
            'htdocs/js/*.js',
            'templates/rbxmlreview/*.txt',
            'templates/rbxmlreview/*.html',
        ],
    }
)
