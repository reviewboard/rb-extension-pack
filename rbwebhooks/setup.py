from setuptools import setup


PACKAGE = "rbwebhooks"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="RBWebHooks, a webhook extension for Review Board",
    author="Steven MacLeod",
    packages=["rbwebhooks"],
    entry_points={
        'reviewboard.extensions':
            '%s = rbwebhooks.extension:RBWebHooksExtension' % PACKAGE,
    },
)
