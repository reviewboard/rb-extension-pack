from setuptools import setup, find_packages

PACKAGE="RB-iPhone"
VERSION="0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="""iPhone UI for Review Board""",
    author="Christian Hammond",
    packages=["rbiphone"],
    entry_points={
        'reviewboard.extensions':
        '%s = rbiphone.extension:IPhoneExtension' % PACKAGE,
    },
    package_data={
        'rbiphone': [
            'htdocs/css/*.css',
            'htdocs/js/*.js',
            'templates/rbiphone/*.html',
        ],
    }
)
