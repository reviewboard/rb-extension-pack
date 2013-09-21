from setuptools import setup


PACKAGE = "reviewboard-together"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Extension reviewboard-together",
    author="None",
    packages=["reviewboard_together"],
    entry_points={
        'reviewboard.extensions':
            '%s = reviewboard_together.extension:ReviewBoardTogether' % PACKAGE,
    },
    package_data={
        'reviewboard_together': [
            'htdocs/css/*.css',
            'htdocs/js/*.js',
            'templates/reviewboard_together/*.txt',
            'templates/reviewboard_together/*.html',
        ],
    }
)
