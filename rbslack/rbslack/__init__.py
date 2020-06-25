"""Version definitions for rbslack."""


from __future__ import unicode_literals


#
# The version of rbslack
#
# This is in the format of:
#
#   (Major, Minor, Micro, Patch, alpha/beta/rc/final, Release Number, Released)
#
VERSION = (0, 1, 0, 0, 'final', 0, True)


def get_version_string():
    """Return the version as a user-visible string.

    Returns:
        unicode:
        The current version.
    """
    version = '%s.%s' % (VERSION[0], VERSION[1])

    if VERSION[2] or VERSION[3]:
        version += ".%s" % VERSION[2]

    if VERSION[3]:
        version += ".%s" % VERSION[3]

    if VERSION[4] != 'final':
        if VERSION[4] == 'rc':
            version += ' RC%s' % VERSION[5]
        else:
            version += ' %s %s' % (VERSION[4], VERSION[5])

    if not is_release():
        version += " (dev)"

    return version


def get_package_version():
    """Return the version for the package.

    Returns:
        unicode:
        The current version.
    """
    version = '%s.%s' % (VERSION[0], VERSION[1])

    if VERSION[2] or VERSION[3]:
        version += ".%s" % VERSION[2]

    if VERSION[3]:
        version += ".%s" % VERSION[3]

    if VERSION[4] != 'final':
        version += '%s%s' % (VERSION[4], VERSION[5])

    return version


def is_release():
    """Return whether this is a release or not.

    Returns:
        bool:
        True if the current version is an official release.
    """
    return VERSION[6]


__version_info__ = VERSION[:-1]
__version__ = get_package_version()
