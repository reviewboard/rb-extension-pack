from __future__ import unicode_literals

import os
import shutil
import sys
import tempfile
from grp import getgrnam
from pwd import getpwnam

from django.conf import settings
from django.core.management import execute_from_command_line
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.diffviewer.models import DiffSet
from reviewboard.reviews.models import (Comment, FileAttachmentComment,
                                        ReviewRequest, Review)
from reviewboard.scmtools.models import Tool


class Command(BaseCommand):
    help = 'Resets the state of the demo server.'

    def handle(self, **options):
        demo_fixtures = getattr(settings, 'DEMO_FIXTURES', None)
        demo_upload_path = getattr(settings, 'DEMO_UPLOAD_PATH', None)
        demo_upload_owner = getattr(settings, 'DEMO_UPLOAD_PATH_OWNER', None)

        if not demo_fixtures:
            raise CommandError(
                'settings.DEMO_FIXTURES must be set to a list of valid '
                'paths')

        if not demo_upload_path or not os.path.exists(demo_upload_path):
            raise CommandError(
                'settings.DEMO_UPLOAD_PATH must be set to a valid path')

        if not demo_upload_owner or len(demo_upload_owner) != 2:
            raise CommandError(
                'settings.DEMO_UPLOAD_PATH_OWNER must be set to '
                '(username, group)')

        # Validate the user and group from DEMO_UPLOAD_PATH_OWNER.
        try:
            uid = getpwnam(demo_upload_owner[0]).pw_uid
            gid = getgrnam(demo_upload_owner[1]).gr_gid
        except KeyError:
            raise CommandError(
                'settings.DEMO_UPLOAD_PATH_OWNER was set to an invalid '
                'username or group.')

        # Check for file permissions on the directories and files we need.
        for fixture in demo_fixtures:
            if not os.access(fixture, os.R_OK):
                raise CommandError(
                    'Fixtures "%s" is not accessible by this user.'
                    % fixture)

        if not os.access(demo_upload_path, os.R_OK):
            raise CommandError(
                'Path "%s" is not accessible by this user.'
                % demo_upload_path)

        dest_uploaded_path = os.path.join(settings.MEDIA_ROOT, 'uploaded')

        for path in (dest_uploaded_path,
                     os.path.join(dest_uploaded_path, '..')):
            if not os.access(path, os.W_OK):
                raise CommandError(
                    'Path "%s" is not writeable by this user.' % path)

        # Check that we can chown files.
        tmpfile = tempfile.mkstemp(prefix='rbdemo-')[1]

        try:
            os.chown(tmpfile, uid, gid)
        except OSError:
            raise CommandError('This user cannot change ownership of files.')
        finally:
            os.unlink(tmpfile)

        cmd = sys.argv[0]

        # Preserve the old site configuration data.
        siteconfig = SiteConfiguration.objects.get_current()

        # Reset the state of the database.
        execute_from_command_line([cmd, 'flush', '--noinput'])
        Tool.objects.all().delete()

        # Now load in the new fixtures.
        execute_from_command_line([cmd, 'loaddata'] + demo_fixtures)

        # Save the siteconfig back out.
        siteconfig.save()

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

        # Replace the uploaded files.
        if os.path.exists(dest_uploaded_path):
            shutil.rmtree(dest_uploaded_path)

        shutil.copytree(demo_upload_path, dest_uploaded_path)

        # Create the images and files directories if they don't exist.
        for dirname in ['images', 'files']:
            path = os.path.join(dest_uploaded_path, dirname)

            if not os.path.exists(path):
                os.mkdir(path)

        # Set ownership for all files and directories.
        for root, dirs, files in os.walk(dest_uploaded_path):
            for path in dirs:
                full_path = os.path.join(root, path)
                os.chown(full_path, uid, gid)
                os.chmod(full_path, 0o755)

            for path in files:
                full_path = os.path.join(root, path)
                os.chown(full_path, uid, gid)
                os.chmod(full_path, 0o644)
