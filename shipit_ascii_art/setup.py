from setuptools import setup


PACKAGE = "shipit_ascii_art"
VERSION = "2.0"

setup(
    name=PACKAGE,
    version=VERSION,
    description="An extension that adds ascii art to Review Board's ship-it "
                "reviews",
    author="Sampson Chen",
    packages=["shipit_ascii_art"],
    entry_points={
        'reviewboard.extensions':
            '%s = shipit_ascii_art.extension:AsciiArt' % PACKAGE,
    },
    python_requires='>=3.7',
    package_data={
        'shipit_ascii_art': [
            'htdocs/css/*.css',
            'htdocs/js/*.js',
            'templates/shipit_ascii_art/*.txt',
            'templates/shipit_ascii_art/*.html',
        ],
    }
)
