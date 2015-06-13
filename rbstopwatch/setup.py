from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup


PACKAGE = "rbstopwatch"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description='Stopwatch extension for Review Board',
    author='Beanbag, Inc. <support@beanbaginc.com>',
    packages=['rbstopwatch'],
    entry_points={
        'reviewboard.extensions':
            '%s = rbstopwatch.extension:StopwatchExtension' % PACKAGE,
    },
    package_data={
        b'rbstopwatch': [
            'templates/rbstopwatch/*.txt',
            'templates/rbstopwatch/*.html',
        ],
    }
)
