from setuptools import setup, find_packages

PACKAGE="RB-Reports"
VERSION="0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="""Reports extension for Review Board""",
    author="Christian Hammond",
    packages=["rbreports"],
    entry_points={
        'reviewboard.extensions':
        '%s = rbreports.extension:ReportsExtension' % PACKAGE,
    },
    package_data={
        'rbreports': [
            'htdocs/css/*.css',
            'htdocs/js/*.js',
            'templates/rbreports/*.html',
            'templates/rbreports/*.txt',
        ],
    }
)
