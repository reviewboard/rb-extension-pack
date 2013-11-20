#!/usr/bin/env python
from setuptools import setup


PACKAGE = "rbwebhooks"
VERSION = "0.2"

setup(
    name=PACKAGE,
    version=VERSION,
    description="RBWebHooks, a webhook extension for Review Board",
    author="Steven MacLeod, Ondrej Kupka",
    packages=["rbwebhooks"],
    install_requires=["requests==2.0.1"],
    entry_points={
        'reviewboard.extensions':
            '%s = rbwebhooks.extension:RBWebHooksExtension' % PACKAGE,
    },
)
