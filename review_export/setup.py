from setuptools import setup


PACKAGE = 'review-export'
VERSION = '0.1'

setup(
    name=PACKAGE,
    version=VERSION,
    description='Add PDF and XML export functionality to Review Board.',
    author='Mark Loyzer',
    packages=['review_export'],
    entry_points={
        'reviewboard.extensions':
            '%s = review_export.extension:ReviewExport' % PACKAGE,
    }
)
