from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup


PACKAGE = 'rbcommenttype'
VERSION = '0.1'

setup(
    name=PACKAGE,
    version=VERSION,
    description='Comment type categorization for Review Board',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=['rbcommenttype'],
    entry_points={
        'reviewboard.extensions':
            '%s = rbcommenttype.extension:CommentTypeExtension' % PACKAGE,
    },
    package_data={
        b'rbcommenttype': [
            'templates/rbcommenttype/*.html',
            'templates/rbcommenttype/*.txt',
        ],
    }
)
