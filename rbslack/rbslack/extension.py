from __future__ import unicode_literals

import json
import logging

from django.contrib.sites.models import Site
from django.utils.six.moves.urllib.request import Request, urlopen
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import SignalHook
from reviewboard.reviews.models import BaseComment, ReviewRequest
from reviewboard.reviews.signals import (review_request_closed,
                                         review_request_published,
                                         review_request_reopened,
                                         review_published,
                                         reply_published)
from reviewboard.site.urlresolvers import local_site_reverse


class SlackExtension(Extension):
    """An extension to integrate Review Board with slack.com"""
    metadata = {
        'Name': 'Slack Integration',
        'Summary': 'Notifies channels on Slack.com for any review '
                   'request activity.',
    }

    is_configurable = True

    default_settings = {
        'webhook_url': '',
        'channel': '',
        'notify_username': 'Review Board',
    }

    def initialize(self):
        """Initialize the extension hooks."""
        hooks = [
            (review_request_closed, self.on_review_request_closed),
            (review_request_published, self.on_review_request_published),
            (review_request_reopened, self.on_review_request_reopened),
            (review_published, self.on_review_published),
            (reply_published, self.on_reply_published),
        ]

        for signal, handler in hooks:
            SignalHook(self, signal, handler)

    def notify(self, text, fields, channel=self.settings['channel']):
        """Send a webhook notification to Slack."""
        payload = {
            'username': self.settings['notify_username'],
            'icon_url': 'http://images.reviewboard.org/rbslack/logo.png',
            'attachments': [
                {
                    'color': '#efcc96',
                    'fallback': text,
                    'fields': fields,
                },
            ],
        }

        payload['channel'] = channel

        logging.info('Notifying channel: {}'.format(channel))

        try:
            urlopen(Request(self.settings['webhook_url'],
                            json.dumps(payload),
                            headers={'Content-type': 'application/json'}))
        except Exception as e:
            logging.error('Failed to send notification to slack.com: %s',
                          e, exc_info=True)

    def format_link(self, path, text):
        """Format the given URL and text to be shown in a Slack message.

        This will combine together the parts of the URL (method, domain, path)
        and format it using Slack's URL syntax.
        """
        siteconfig = SiteConfiguration.objects.get_current()
        site = Site.objects.get_current()

        # Slack only wants these three entities replaced, rather than
        # all the entities that Django's escape() would attempt to replace.
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')

        return '<%s://%s%s|%s>' % (
            siteconfig.get('site_domain_method'),
            site.domain,
            path,
            text)

    def get_user_text_link(self, user, local_site):
        """Get the Slack-formatted link to a user page."""
        # This doesn't use user.get_absolute_url because that won't include
        # site roots or local site names.
        if local_site:
            local_site_name = local_site.name
        else:
            local_site_name = None

        user_url = local_site_reverse(
            'user',
            local_site_name=local_site_name,
            kwargs={'username': user.username})

        return self.format_link(
            user_url,
            user.get_full_name() or user.username)

    def get_review_request_text_link(self, review_request):
        """Get the Slack-formatted link to a review request."""
        return self.format_link(
            review_request.get_absolute_url(),
            review_request.summary)

    def on_review_request_closed(self, user, review_request, type, **kwargs):
        """Handler for the review_request_closed signal."""
        if type == ReviewRequest.DISCARDED:
            close_type = 'Discarded'
        elif type == ReviewRequest.SUBMITTED:
            close_type = 'Submitted'
        else:
            logging.error('rbslack: Tried to notify on review_request_closed '
                          'for review request pk=%d with unknown close type '
                          '"%s"',
                          review_request.pk, type)
            return

        if not user:
            user = review_request.submitter

        review_request_link = self.get_review_request_text_link(review_request)
        user_link = self.get_user_text_link(user, review_request.local_site)
        fields = [
            {
                'title': 'Review Request Closed',
                'value': review_request_link,
                'short': False,
            },
            {
                'title': 'By',
                'value': user_link,
                'short': True,
            },
            {
                'title': 'Closed As',
                'value': close_type,
                'short': True,
            },
        ]
        text = 'Review Request %s: %s' % (close_type, review_request_link)

        logging.debug('Notifying slack.com for event review_request_closed: '
                      'review_request pk=%d',
                      review_request.pk)
        self.notify_all(text, fields, review_request)

    def on_review_request_published(self, user, review_request, changedesc,
                                    **kwargs):
        """Handler for the review_request_published signal."""
        review_request_link = self.get_review_request_text_link(review_request)
        user_link = self.get_user_text_link(user, review_request.local_site)
        fields = [
            {
                'title': 'Review Request Published',
                'value': review_request_link,
                'short': False,
            },
            {
                'title': 'By',
                'value': user_link,
                'short': True,
            },
        ]
        text = 'Review Request Published: %s' % review_request_link

        logging.debug('Notifying slack.com for event '
                      'review_request_published: review_request pk=%d',
                      review_request.pk)
        self.notify_all(text, fields, review_request)

    def on_review_request_reopened(self, user, review_request, **kwargs):
        """Handler for the review_request_reopened signal."""
        if not user:
            user = review_request.submitter

        review_request_link = self.get_review_request_text_link(review_request)
        user_link = self.get_user_text_link(user, review_request.local_site)
        fields = [
            {
                'title': 'Review Request Reopened',
                'value': review_request_link,
                'short': False,
            },
            {
                'title': 'By',
                'value': user_link,
                'short': True,
            },
        ]
        text = 'Review Request Reopened: %s' % review_request_link

        logging.debug('Notifying slack.com for event review_request_reopened: '
                      'review_request pk=%d',
                      review_request.pk)
        self.notify_all(text, fields, review_request)

    def notify_review(self, user, review, title, extra_fields=[],
                      extra_text=''):
        """Helper to do the common part of reviews and replies."""
        review_request = review.review_request
        review_request_link = self.get_review_request_text_link(review_request)
        user_link = self.get_user_text_link(user, review_request.local_site)
        fields = [
            {
                'title': title,
                'value': review_request_link,
                'short': False,
            },
            {
                'title': 'By',
                'value': user_link,
                'short': True,
            },
        ] + extra_fields

        text = '%s: %s%s' % (title, review_request_link, extra_text)

        self.notify_all(text, fields, review_request)

    def on_review_published(self, user, review, **kwargs):
        """Handler for the review_published signal."""
        logging.debug('Notifying slack.com for event review_published: '
                      'review pk=%d',
                      review.pk)

        open_issues = 0
        for comment in review.get_all_comments():
            if (comment.issue_opened and
                comment.issue_status == BaseComment.OPEN):
                open_issues += 1

        if open_issues == 1:
            issue_text = '1 issue'
        else:
            issue_text = '%d issues' % open_issues

        # There doesn't seem to be any image support inside the text fields,
        # but the :white_check_mark: emoji shows a green box with a check-mark
        # in it, and the :warning: emoji is a yellow exclamation point, which
        # are close enough.
        if review.ship_it:
            if open_issues:
                extra_fields = [{
                    'title': 'Fix it, then Ship it!',
                    'value': ':warning: %s' % issue_text,
                    'short': True,
                }]
                extra_text = ' (Fix it, then Ship it!)'
            else:
                extra_fields = [{
                    'title': 'Ship it!',
                    'value': ':white_check_mark:',
                    'short': True,
                }]
                extra_text = ' (Ship it!)'
        elif open_issues:
            extra_fields = [{
                'title': 'Open Issues',
                'value': ':warning: %s' % issue_text,
                'short': True,
            }]
            extra_text = '(%s)' % issue_text
        else:
            extra_fields = []
            extra_text = ''

        self.notify_review(user, review, 'Review Published',
                           extra_fields=extra_fields,
                           extra_text=extra_text)

    def on_reply_published(self, user, reply, **kwargs):
        """Handler for the reply_published signal."""
        logging.debug('Notifying slack.com for event reply_published: '
                      'review pk=%d',
                      reply.pk)
        self.notify_review(user, reply, 'Reply Published')

    def notify_all(self, text, fields, review_request):
        """Notify all people and groups associated with the review
           This assumes the usernames in Slack and ReviewBoard match
        """
        self.notify(text, fields)

        notify_list = [review_request.submitter.username, ]

        for user in set(review_request.get_participants()):
            notify_list.append(user.username)

        for group in review_request.target_groups.all():
            for user in group.users.all():
                notify_list.append(user.username)

        for username in set(notify_list):
            self.notify(text, fields, '@{username}'.format(
                username=username))
