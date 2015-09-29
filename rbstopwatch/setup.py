from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup

from rbstopwatch import get_package_version


setup(
    name='rbstopwatch',
    version=get_package_version(),
    description='Stopwatch extension for Review Board',
    url='https://www.reviewboard.org/',
    author='Beanbag, Inc.',
    author_email='support@beanbaginc.com',
    maintainer='Beanbag, Inc.',
    maintainer_email='support@beanbaginc.com',
    packages=[b'rbstopwatch'],
    entry_points={
        'reviewboard.extensions': [
            'rbstopwatch = rbstopwatch.extension:StopwatchExtension',
        ],
    },
    package_data={
        b'rbstopwatch': [
            'templates/rbstopwatch/*.txt',
            'templates/rbstopwatch/*.html',
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
