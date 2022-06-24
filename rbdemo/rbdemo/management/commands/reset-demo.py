"""Command to reset the state of the demo server."""

import base64
import bz2
import os
import shutil
import tempfile
from collections import OrderedDict
from grp import getgrnam
from pwd import getpwnam

import yaml
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.db import connection, transaction
from djblets.secrets.crypto import aes_decrypt_base64
from reviewboard.attachments.models import (FileAttachment,
                                            FileAttachmentHistory)
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.diffviewer.differ import DiffCompatVersion
from reviewboard.diffviewer.models import (DiffSet,
                                           DiffSetHistory,
                                           FileDiff)
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.reviews.models import (Comment,
                                        FileAttachmentComment,
                                        Group,
                                        Review,
                                        ReviewRequest)
from reviewboard.scmtools.crypto_utils import encrypt_password
from reviewboard.scmtools.models import Repository, Tool


class Command(BaseCommand):
    """Command to reset the state of the demo server."""

    help = 'Resets the state of the demo server.'

    def handle(self, **options):
        """Run the command.

        Args:
            **options (dict):
                Options for the command.
        """
        aes_key = getattr(settings, 'DEMO_AES_KEY', None)
        demo_fixtures = getattr(settings, 'DEMO_FIXTURES', None)
        demo_upload_path = getattr(settings, 'DEMO_UPLOAD_PATH', None)
        demo_upload_owner = getattr(settings, 'DEMO_UPLOAD_PATH_OWNER', None)

        if not aes_key or len(aes_key) != 32:
            raise CommandError(
                'settings.DEMO_AES_KEY must be set to 32 characters.')

        if isinstance(aes_key, str):
            aes_key = aes_key.encode('ascii')

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

        self.stdout.write('Reloading demo data...')

        with transaction.atomic(using=connection.alias):
            with connection.cursor() as cursor:
                # First, reset the database back to a near-blank slate.
                self._reset_database(cursor)

                # Next, load the media files, so we can refer to these
                # files when loading demo data.
                self._load_media_files(source_path=demo_upload_path,
                                       dest_path=dest_uploaded_path,
                                       uid=uid,
                                       gid=gid)

                # Now we can load the demo data.
                self._load_demo_data(demo_fixtures, aes_key=aes_key)

        self.stdout.write('Demo data has been loaded into the database.\n')

    def _reset_database(self, cursor):
        """Reset the state of the database.

        This will erase and reset sequences for most tables in the database,
        with the exception of a handful of base-level tables used for
        base server configuration and evolution/migration history.

        Args:
            cursor (django.db.backends.util.CursorWrapper):
                The current database cursor.
        """
        # Reset almost all the tables.
        keep_tables = {
            'django_content_type',
            'django_evolution',
            'django_migrations',
            'django_project_version',
            'django_site',
            'extensions_registeredextension',
            'scmtools_tool',
            'siteconfig_siteconfiguration',
        }

        all_tables = connection.introspection.django_table_names(
            only_existing=True,
            include_views=False)

        tables = [
            _table
            for _table in all_tables
            if _table not in keep_tables
        ]

        # Flush the tables and reset their sequences.
        flush = connection.ops.sql_flush(
            style=no_style(),
            tables=tables,
            reset_sequences=True,
            allow_cascade=True)

        for sql in flush:
            cursor.execute(sql)

    def _load_media_files(self, source_path, dest_path, uid, gid):
        """Load bundled media files for file attachments.

        This will copy over all uploaded media files into the site, changing
        ownership to match that of the site in the process.

        Args:
            source_path (str):
                The source path for the uploaded media files.

            dest_path (str):
                The destination path to copy the files into.

            uid (int):
                The User ID for uploaded files.

            gid (int):
                The Group ID for uploaded files.
        """
        shutil.copytree(source_path, dest_path,
                        dirs_exist_ok=True)

        # Create the images and files directories if they don't exist.
        for dirname in ['images', 'files']:
            path = os.path.join(dest_path, dirname)

            if not os.path.exists(path):
                os.mkdir(path)

        # Set ownership for all files and directories.
        for root, dirs, files in os.walk(dest_path):
            for path in dirs:
                full_path = os.path.join(root, path)
                os.chown(full_path, uid, gid)
                os.chmod(full_path, 0o755)

            for path in files:
                full_path = os.path.join(root, path)
                os.chown(full_path, uid, gid)
                os.chmod(full_path, 0o644)

    def _load_demo_data(self, filenames, *, aes_key):
        """Load data from a demo fixture.

        This will open the provided YAML files, loading all users, groups,
        hosting service accounts, repositories, review requests, reviews,
        file attachments, diffs, and so on.

        The list of files will be opened in order. User, group, hosting
        service account, and repository state can be reused in subsequent
        data files.

        Passwords and hosting service account data must be encrypted using
        ``aes_key``.

        Args:
            filenames (list of str):
                The list of data filenames to load.

            aes_key (bytes):
                The key used for encrypted state.
        """
        users_map = {}
        groups_map = {}
        hosting_accounts_map = {}
        repositories_map = {}

        # Load the tools.
        tools_map = {
            _tool.scmtool_id: _tool
            for _tool in Tool.objects.all()
        }

        for filename in filenames:
            with open(filename, 'r') as fp:
                fixture_data = yaml.load(fp, Loader=yaml.FullLoader)

            # Load the users.
            users_map.update(self._load_users(
                fixture_data.get('users', []),
                aes_key=aes_key))

            # Load the review groups.
            groups_map.update(self._load_groups(
                fixture_data.get('review_groups', []),
                users_map=users_map))

            # Load the hosting service accounts.
            hosting_accounts_map.update(self._load_hosting_service_accounts(
                fixture_data.get('hosting_service_accounts', []),
                aes_key=aes_key))

            # Load the repositories.
            repositories_map.update(self._load_repositories(
                fixture_data.get('repositories', []),
                tools_map=tools_map,
                hosting_accounts_map=hosting_accounts_map))

            # Load the review requests.
            self._load_review_requests(fixture_data.get('review_requests', []),
                                       users_map=users_map,
                                       groups_map=groups_map,
                                       repositories_map=repositories_map)

    def _load_users(self, data, *, aes_key):
        """Load users from data.

        Args:
            data (list of dict):
                The data from which to load lists of users.

            aes_key (bytes):
                The key used for encrypted state.

        Returns:
            dict:
            A resulting map of usernames to saved user instances.
        """
        users_map = {}

        for user_data in data:
            password = user_data.pop('password', None)

            user = User(**user_data)

            if password:
                user.password = aes_decrypt_base64(password, key=aes_key)
            else:
                user.set_unusable_password()

            user.save()
            users_map[user.username] = user

        return users_map

    def _load_groups(self, data, *, users_map):
        """Load review groups from data.

        Args:
            data (list of dict):
                The data from which to load lists of review groups.

            users_map (dict):
                A users map built from :py:meth:`_load_users`.

        Returns:
            dict:
            A resulting map of group names to group instances.
        """
        groups_map = {}

        for group_data in data:
            group_users = group_data.pop('users', [])

            group = Group.objects.create(**group_data)
            groups_map[group.name] = group

            if group_users:
                group.users.add(*[
                    users_map[_username]
                    for _username in group_users
                ])

        return groups_map

    def _load_hosting_service_accounts(self, data, *, aes_key):
        """Load hosting service accounts from data.

        Args:
            data (list of dict):
                The data from which to load lists of hosting service accounts.

            aes_key (bytes):
                The key used for encrypted state.

        Returns:
            dict:
            A resulting map of pairs of ``(service_name, username)`` to
            hosting service account instances.
        """
        hosting_accounts_map = {}

        for hosting_account_data in data:
            service_data = hosting_account_data.pop('data')
            norm_service_data = {}

            for key, info in service_data.items():
                assert isinstance(info, dict)

                value = info['value']
                value_type = info['type']
                store_as = info['store_as']

                if value_type == 'encrypted':
                    value = aes_decrypt_base64(value, key=aes_key)

                if store_as == 'encrypted_password':
                    value = encrypt_password(value)

                norm_service_data[key] = value

            hosting_account = HostingServiceAccount.objects.create(
                data=norm_service_data,
                **hosting_account_data)

            key = (hosting_account.service_name, hosting_account.username)
            hosting_accounts_map[key] = hosting_account

        return hosting_accounts_map

    def _load_repositories(self, data, *, tools_map, hosting_accounts_map):
        """Load repositories from data.

        Args:
            data (list of dict):
                The data from which to load lists of repositories.

            tools_map (dict):
                A mapping of SCMTool IDs to
                :py:class:`~reviewboard.scmtools.models.Tool` instances.

            hosting_accounts_map (dict):
                A hosting service accounts map built from
                :py:meth:`_load_hosting_service_accounts`.

        Returns:
            dict:
            A resulting mapping of repository names to instances.
        """
        repositories_map = {}

        for repository_data in data:
            scmtool_id = repository_data['scmtool_id']
            hosting_account = repository_data.pop('hosting_account', None)

            if hosting_account is not None:
                key = (hosting_account.get('service'),
                       hosting_account.get('username'))

                hosting_account = hosting_accounts_map[key]

            repository = Repository.objects.create(
                hosting_account=hosting_account,
                tool=tools_map[scmtool_id],
                **repository_data)

            repositories_map[repository.name] = repository

        return repositories_map

    def _load_review_requests(self, data, *, users_map, groups_map,
                              repositories_map):
        """Load review requests and related objects from data.

        This will load review requests and all associated data, along with
        diffs, review history, and change descriptions.

        Args:
            data (list of dict):
                The data from which to load lists of review requests.

            users_map (dict):
                A users map built from :py:meth:`_load_users`.

            groups_map (dict):
                A review groups map built from :py:meth:`_load_groups`.

            repositories_map (dict):
                A repositories map built from :py:meth:`_load_repositories`.
        """
        for review_request_data in data:
            submitter = users_map[review_request_data.pop('owner')]
            target_groups_data = review_request_data.pop('target_groups', [])
            target_people_data = review_request_data.pop('target_people', [])
            file_attachment_histories_data = review_request_data.pop(
                'file_attachment_histories', [])
            diffsets_data = review_request_data.pop('diffsets', [])
            depends_on_data = review_request_data.pop('depends_on', [])
            entries_data = review_request_data.pop('entries', [])
            repository = review_request_data.pop('repository', None)

            if repository is not None:
                repository = repositories_map[repository]

            diffset_history = DiffSetHistory.objects.create()

            # Note that we can't use ReviewRequest.objects.create(), as that
            # is overridden and specialized, and we don't want to invoke
            # that behavior here.
            review_request = ReviewRequest(
                submitter=submitter,
                diffset_history=diffset_history,
                repository=repository,
                **review_request_data)
            review_request.save()

            # Load the target reviewers.
            if target_groups_data:
                review_request.target_groups.add(*[
                    groups_map[_group_name]
                    for _group_name in target_groups_data
                ])

            if target_people_data:
                review_request.target_people.add(*[
                    users_map[_username]
                    for _username in target_people_data
                ])

            if depends_on_data:
                review_request.depends_on.add(*depends_on_data)

            # Load the file attachment histories.
            file_attachments_map = self._load_file_attachment_histories(
                file_attachment_histories_data,
                review_request=review_request)

            if file_attachments_map:
                review_request.file_attachments.add(
                    *file_attachments_map.values())

            # Load the diffsets.
            diffsets_map, filediffs_map = self._load_diffsets(
                diffsets_data,
                repository=repository,
                diffset_history=diffset_history)

            # Load the entries (reviews, change descriptions).
            self._load_entries(entries_data,
                               review_request=review_request,
                               users_map=users_map,
                               diffsets_map=diffsets_map,
                               filediffs_map=filediffs_map,
                               file_attachments_map=file_attachments_map)

    def _load_file_attachment_histories(self, data, *, review_request):
        """Load file attachment histories and related objects from data.

        This will load file attachment histories and all contained file
        attachments.

        Args:
            data (list of dict):
                The data from which to load lists of file attachment
                histories.

            review_request (reviewboard.reviews.models.ReviewRequest):
                The review request that owns these file attachment histories.

        Returns:
            dict:
            A resulting mapping of file attachment filenames to instances.
        """
        file_attachments_map = OrderedDict()
        file_attachment_histories = []

        for i, file_attachment_history_data in enumerate(data):
            file_attachments_data = \
                file_attachment_history_data.get('file_attachments', [])

            file_attachment_history = FileAttachmentHistory.objects.create(
                display_position=i,
                latest_revision=0)
            file_attachment_histories.append(file_attachment_history)

            file_attachments_map.update(
                self._load_file_attachments(
                    file_attachments_data,
                    file_attachment_history=file_attachment_history))

        review_request.file_attachment_histories.add(
            *file_attachment_histories)

        return file_attachments_map

    def _load_file_attachments(self, data, *, file_attachment_history):
        """Load file attachments from data.

        This will load file attachment histories and all contained file
        attachments.

        Args:
            data (list of dict):
                The data from which to load lists of file attachments.

            file_attachment_history (reviewboard.attachments.models.
                                     FileAttachmentHistory):
                The history that owns these file attachments.

        Returns:
            dict:
            A resulting mapping of file attachment filenames to instances.
        """
        file_attachments_map = OrderedDict()

        for revision, file_attachment_data in enumerate(data, start=1):
            file_attachment = FileAttachment.objects.create(
                attachment_history=file_attachment_history,
                attachment_revision=revision,
                **file_attachment_data)

            key = (revision, file_attachment.orig_filename)
            file_attachments_map[key] = file_attachment

        return file_attachments_map

    def _load_diffsets(self, data, *, repository, diffset_history):
        """Load diffsets and related objects from data.

        This will load diffsets, contained filediffs, and diff data.

        Args:
            data (list of dict):
                The data from which to load lists of diffsets.

            repository (reviewboard.scmtools.models.Repository):
                The repository that the diffsets will be associated with.

            diffset_history (reviewboard.diffviewer.models.DiffSetHistory):
                The history that owns these diffsets.

        Returns:
            tuple:
            A 2-tuple containing:

            1. A dictionary mapping diffset revisions to instances.
            2. A dictionary mapping filediffs to instances (see
               :py:meth:`_load_filediffs`).
        """
        diffsets_map = {}
        filediffs_map = {}

        for revision, diffset_data in enumerate(data, start=1):
            filediffs_data = diffset_data.pop('filediffs')
            diffset = DiffSet.objects.create(
                history=diffset_history,
                revision=revision,
                repository=repository,
                diffcompat=DiffCompatVersion.DEFAULT,
                **diffset_data)
            diffsets_map[revision] = diffset

            filediffs_map.update(
                self._load_filediffs(filediffs_data,
                                     diffset=diffset))

        return diffsets_map, filediffs_map

    def _load_filediffs(self, data, *, diffset):
        """Load filediffs from data.

        This will load filediffs and diff data.

        Args:
            data (list of dict):
                The data from which to load lists of filediffs.

            diffset (reviewboard.diffviewer.models.DiffSet):
                The diffset that owns these filediffs.

        Returns:
            dict:
            A resulting mapping of pairs of ``(diffset_revision, source_file)``
            to filediff instances.
        """
        scmtool = diffset.repository.get_scmtool()
        filediffs_map = {}

        for filediff_data in data:
            diff_data = bz2.decompress(base64.b64decode(
                filediff_data.pop('diff')))

            filediff = FileDiff.objects.create(
                diffset=diffset,
                diff=diff_data,
                **filediff_data)

            key = (diffset.revision, filediff.source_file)
            filediffs_map[key] = filediff

            filediff.diff_hash.recalculate_line_counts(scmtool)

        return filediffs_map

    def _load_entries(self, data, **kwargs):
        """Load entries for a review request from data.

        This will load reviews and change descriptions in the proper order
        to be shown on the review request page.

        Args:
            data (list of dict):
                The data from which to load lists of filediffs.

            **kwargs (dict):
                Arguments to pass to :py:meth:`_load_review` and
                :py:meth:`_load_change_description`.
        """
        for entry_data in data:
            entry_type = entry_data.pop('entry_type')

            if entry_type == 'review':
                self._load_review(entry_data, **kwargs)
            elif entry_type == 'change_description':
                self._load_change_description(entry_data, **kwargs)

    def _load_review(self, data, *, review_request, users_map,
                     filediffs_map, file_attachments_map,
                     reply_to_review=None,
                     reply_to_diff_comments_map={},
                     reply_to_file_attachment_comments_map={},
                     **kwargs):
        """Load a review and its replies and comments from data.

        Args:
            data (dict):
                The data from which to load a review or reply.

            review_request (reviewboard.reviews.models.ReviewRequest):
                The review request that owns this review.

            users_map (dict):
                A users map built from :py:meth:`_load_users`.

            filediffs_map (dict):
                A filediffs map built from :py:meth:`_load_filediffs`.

            file_attachments_map (dict):
                A file attachments map built from
                :py:meth:`_load_file_attachments`.

            reply_to_review (reviewboard.reviews.models.Review, optional):
                A review that this is replying to, if this is a reply.

            reply_to_diff_comments_map (dict):
                A diff comments map built from :py:meth:`_load_diff_comments`.

            reply_to_file_attachment_comments_map (dict):
                A file attachment comments map built from
                :py:meth:`_load_file_attachment_comments`.

            **kwargs (dict, unused):
                Additional unused arguments.
        """
        user = users_map[data.pop('user')]
        replies = data.pop('replies', [])
        diff_comments_data = data.pop('diff_comments', [])
        file_attachment_comments_data = data.pop('file_attachment_comments',
                                                 [])

        review = Review.objects.create(
            user=user,
            base_reply_to=reply_to_review,
            review_request=review_request,
            **data)

        diff_comments_map = self._load_diff_comments(
            diff_comments_data,
            review=review,
            filediffs_map=filediffs_map,
            reply_to_comments_map=reply_to_diff_comments_map)

        file_attachment_comments_map = self._load_file_attachment_comments(
            file_attachment_comments_data,
            review=review,
            file_attachments_map=file_attachments_map,
            reply_to_comments_map=reply_to_file_attachment_comments_map)

        if replies:
            for reply_data in replies:
                self._load_review(
                    reply_data,
                    review_request=review_request,
                    users_map=users_map,
                    filediffs_map=filediffs_map,
                    file_attachments_map=file_attachments_map,
                    reply_to_review=review,
                    reply_to_diff_comments_map=diff_comments_map,
                    reply_to_file_attachment_comments_map=(
                        file_attachment_comments_map))

    def _load_change_description(self, data, *, review_request, users_map,
                                 diffsets_map, filediffs_map,
                                 file_attachments_map, **kwargs):
        """Load a change description from data.

        Args:
            data (dict):
                The data from which to load a change description.

            review_request (reviewboard.reviews.models.ReviewRequest):
                The review request that owns this change description.

            users_map (dict):
                A users map built from :py:meth:`_load_users`.

            diffsets_map (dict):
                A diffsets map built from :py:meth:`_load_diffsets`.

            filediffs_map (dict):
                A filediffs map built from :py:meth:`_load_filediffs`.

            file_attachments_map (dict):
                A file attachments map built from
                :py:meth:`_load_file_attachments`.

            **kwargs (dict, unused):
                Additional unused arguments.
        """
        user = users_map[data.pop('user')]
        fields_changed = data['fields_changed']

        if 'files' in fields_changed:
            files_changed = fields_changed['files']

            for key in ('old', 'new', 'removed', 'added'):
                items = files_changed.get(key, [])

                for i, file_attachment_ref in enumerate(list(items)):
                    key = (file_attachment_ref['revision'],
                           file_attachment_ref['filename'])
                    file_attachment = file_attachments_map[key]

                    items[i] = [
                        file_attachment.caption,
                        file_attachment.file.url,
                        file_attachment.pk,
                    ]

        if 'diff' in fields_changed:
            diff_changed = fields_changed['diff']

            for key in ('removed', 'added'):
                items = diff_changed.get(key, [])

                for item in items:
                    diffset = diffsets_map[item[2]]
                    item[2] = diffset.pk

        changedesc = ChangeDescription.objects.create(user=user, **data)
        review_request.changedescs.add(changedesc)

    def _load_diff_comments(self, data, *, review, filediffs_map,
                            reply_to_comments_map={}):
        """Load a list of diff comments from data.

        Args:
            data (list of dict):
                The data from which to load a list of diff comments.

            review (reviewboard.reviews.models.Review):
                The review that owns these comments.

            filediffs_map (dict):
                A filediffs map built from :py:meth:`_load_filediffs`.

            reply_to_comments_map (dict):
                A diff comments map built from this method, if this is a
                reply.

        Returns:
            dict:
            A resulting dictionary mapping pairs of ``(diffset_revision,
            source_file)`` to diff comment instances.
        """
        comments_map = {}
        comments = []

        for comment_data in data:
            filediff_data = comment_data.pop('filediff')

            key = (filediff_data['revision'], filediff_data['source_file'])
            filediff = filediffs_map[key]

            comment = Comment.objects.create(
                filediff=filediff,
                reply_to=reply_to_comments_map.get(key),
                **comment_data)
            comments.append(comment)
            comments_map[key] = comment

        review.comments.add(*comments)

        return comments_map

    def _load_file_attachment_comments(self, data, *, review,
                                       file_attachments_map,
                                       reply_to_comments_map={}):
        """Load a list of file attachment comments from data.

        Args:
            data (list of dict):
                The data from which to load a list of file attachment
                comments.

            review (reviewboard.reviews.models.Review):
                The review that owns these comments.

            file_attachments_map (dict):
                A file attachments map built from
                :py:meth:`_load_file_attachments`.

            reply_to_comments_map (dict):
                A diff comments map built from this method, if this is a
                reply.

        Returns:
            dict:
            A resulting dictionary mapping file attachment filenames to
            file attachment comment instances.
        """
        comments_map = {}
        comments = []

        for comment_data in data:
            file_attachment_ref = comment_data.pop('file_attachment')

            file_attachment_key = (
                file_attachment_ref['revision'],
                file_attachment_ref['filename'],
            )
            file_attachment = file_attachments_map[file_attachment_key]

            if 'diff_against_revision' in file_attachment_ref:
                diff_against_file_attachment_key = (
                    file_attachment_ref['diff_against_revision'],
                    file_attachment_ref['filename'],
                )
                diff_against_file_attachment = \
                    file_attachments_map[diff_against_file_attachment_key]
            else:
                diff_against_file_attachment = None

            comment_key = file_attachment.orig_filename

            comment = FileAttachmentComment.objects.create(
                file_attachment=file_attachment,
                diff_against_file_attachment=diff_against_file_attachment,
                reply_to=reply_to_comments_map.get(comment_key),
                **comment_data)
            comments.append(comment)
            comments_map[comment_key] = comment

        review.file_attachment_comments.add(*comments)

        return comments_map
