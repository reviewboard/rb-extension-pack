from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup

from rbcommenttype import get_package_version


setup(
    name='rbcommenttype',
    version=get_package_version(),
    description='Comment type categorization for Review Board',
    url='https://www.reviewboard.org/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=[b'rbcommenttype'],
    entry_points={
        'reviewboard.extensions': [
            'rbcommenttype = rbcommenttype.extension:CommentTypeExtension',
        ]
    },
    package_data={
        b'rbcommenttype': [
            'templates/rbcommenttype/*.html',
            'templates/rbcommenttype/*.txt',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Review Board',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
