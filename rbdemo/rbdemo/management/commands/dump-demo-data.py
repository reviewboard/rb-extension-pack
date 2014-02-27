from __future__ import unicode_literals

import sys

from django.core.management import execute_from_command_line
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = 'Dumps the contents of the demo server for use in resets.'

    EXCLUDE_APPS = [
        'contenttypes',
    ]

    def handle_noargs(self, **options):
        # Reset the state of the database.
        cmd = [sys.argv[0], 'dumpdata', '--indent=2']

        for app in self.EXCLUDE_APPS:
            cmd += ['-e', app]

        execute_from_command_line(cmd)
