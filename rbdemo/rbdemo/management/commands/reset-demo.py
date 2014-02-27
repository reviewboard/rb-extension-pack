from __future__ import unicode_literals

import os
import shutil
import sys

from django.conf import settings
from django.core.management import execute_from_command_line
from django.core.management.base import CommandError, NoArgsCommand
from django.utils import timezone
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.diffviewer.models import DiffSet
from reviewboard.reviews.models import (Comment, FileAttachmentComment,
                                        ReviewRequest, Review)


class Command(NoArgsCommand):
    help = 'Resets the state of the demo server.'

    def handle_noargs(self, **options):
        demo_fixtures = getattr(settings, 'DEMO_FIXTURES', None)
        demo_upload_path = getattr(settings, 'DEMO_UPLOAD_PATH', None)
        demo_upload_owner = getattr(settings, 'DEMO_UPLOAD_PATH_OWNER', None)

        if not demo_fixtures:
            raise CommandError(
                'settings.DEMO_FIXTURES must be set to a list of valid '
                'paths')

        if not demo_upload_path or not os.path.exists(demo_upload_path)
            raise CommandError(
                'settings.DEMO_UPLOAD_PATH must be set to a valid path')

        if not demo_upload_owner:
            raise CommandError(
                'settings.DEMO_UPLOAD_PATH_OWNER must be set to '
                '(uid, gid)')

        cmd = sys.argv[0]

        # Reset the state of the database.
        execute_from_command_line([cmd, 'flush', '--noinput',
                                   '--no-initial-data'])

        # Now load in the new fixtures.
        execute_from_command_line([cmd, 'loaddata'] + demo_fixtures)

        # Update the timestamps on everything.
        now = timezone.now()

        ReviewRequest.objects.update(
            time_added=now,
            last_updated=now,
            last_review_activity_timestamp=now)
        Review.objects.update(timestamp=now)
        Comment.objects.update(timestamp=now)
        FileAttachmentComment.objects.update(timestamp=now)
        ChangeDescription.objects.update(timestamp=now)
        DiffSet.objects.update(timestamp=now)

        # Replace the uploaded filess.
        dest_uploaded_path = os.path.join(settings.MEDIA_ROOT, 'uploaded')

        if os.path.exists(dest_uploaded_path):
            shutil.rmtree(dest_uploaded_path)

        shutil.copytree(demo_upload_path, dest_uploaded_path)
        os.chown(demo_upload_path, *demo_upload_owner)
