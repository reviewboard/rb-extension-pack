"""Models for the rbwebhooks extension."""

from __future__ import unicode_literals

from django.db import models

from rbwebhooks.handlers import SignalHandlers


class WebHookTarget(models.Model):
    """A target for a Web Hook.

    A Web Hook Target is a URL, and other meta data, which will be POST
    requested when the coresponding event fires.

    The corresponding event is specified in hook_id, which should be the name
    of the signal for the hook.
    """

    hook_id = models.CharField('hook type', max_length=128,
                               choices=SignalHandlers.HOOK_CHOICES)
    description = models.CharField(max_length=512, default='', blank=True)
    url = models.URLField('URL')
    enabled = models.BooleanField()

    class Meta:
        app_label = 'rbwebhooks'
        verbose_name = 'Web Hook Target'
        verbose_name_plural = 'Web Hook Targets'
