from setuptools import setup, find_packages

PACKAGE="RB-CIA"
VERSION="0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="""CIA extension for Review Board""",
    author="Christian Hammond",
    packages=["rbcia"],
    entry_points={
        'reviewboard.extensions':
        '%s = rbcia.extension:CIAExtension' % PACKAGE,
    },
    package_data={
        'rbreports': [
            'templates/rbcia/*.html',
        ],
    }
)
