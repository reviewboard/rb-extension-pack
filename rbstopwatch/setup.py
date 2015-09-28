from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup

from rbstopwatch import get_package_version


PACKAGE = "rbstopwatch"


setup(
    name=PACKAGE,
    version=get_package_version(),
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
