"""Comment severity extension for Review Board."""


# The version of rbseverity.
#
# This is in the format of:
#
#   (Major, Minor, Micro, Patch, alpha/beta/rc/final, Release Number, Released)
#
VERSION = (2, 0, 0, 0, 'alpha', 0, False)


def get_version_string():
    """Return the version as a string.

    Returns:
        str:
        The version number, formatted as a string.
    """
    major, minor, micro, patch, tag, relnum, is_release = VERSION

    version = '%s.%s' % (major, minor)

    if micro or patch:
        version += '.%s' % micro

        if patch:
            version += '.%s' % patch

        if tag != 'final':
            if tag == 'rc':
                version += ' RC'
            else:
                version += ' %s ' % tag

            version += '%s' % relnum

    if not is_release:
        version += ' (dev)'

    return version


def get_package_version():
    """Return the package version as a string.

    Returns:
        str:
        The package version number, formatted as a string.
    """
    major, minor, micro, patch, tag, relnum = VERSION[:-1]

    version = '%s.%s' % (major, minor)

    if micro or patch:
        version += '.%s' % micro

        if patch:
            version += '.%s' % patch

    if tag != 'final':
        version += '%s%s' % (
            {
                'alpha': 'a',
                'beta': 'b',
            }.get(tag, tag),
            relnum)

    return version


def is_release():
    """Return whether this is a final release.

    Returns:
        bool:
        ``True`` if this version is a final release. ``False`` if built from
        git or a prerelease.
    """
    return VERSION[-1]


__version_info__ = VERSION[:-1]
__version__ = get_package_version()
