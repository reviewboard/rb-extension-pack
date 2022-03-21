from reviewboard.extensions.packaging import setup


PACKAGE = 'rb-user-stats'
VERSION = '1.0'

setup(
    name=PACKAGE,
    version=VERSION,
    description='Show statistics for Review Board users in the infobox',
    url='https://www.reviewboard.org/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=['rb_user_stats'],
    python_requires='>=3.7',
    entry_points={
        'reviewboard.extensions':
            '%s = rb_user_stats.extension:RBUserStats' % PACKAGE,
    },
    package_data={
        'rb_user_stats': [
            'templates/rb_user_stats/*.html',
        ],
    }
)
