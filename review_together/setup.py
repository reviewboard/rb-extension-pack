from reviewboard.extensions.packaging import setup


PACKAGE = "review-together"
VERSION = "2.0"


setup(
    name=PACKAGE,
    version=VERSION,
    description="Add chat functionality to Review Board",
    author="Mike Conley",
    packages=["review_together"],
    entry_points={
        'reviewboard.extensions':
            '%s = review_together.extension:ReviewTogether' % PACKAGE,
    },
    python_requires='>=3.7',
    package_data={
        'review_together': [
            'htdocs/css/*.css',
            'htdocs/js/*.js',
            'templates/review_together/*.txt',
            'templates/review_together/*.html',
        ],
    }
)
