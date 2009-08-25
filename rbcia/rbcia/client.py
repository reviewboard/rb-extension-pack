from django.conf import settings
from django.contrib.sites.models import Site
from django.dispatch import dispatcher
import xmlrpclib

from reviewboard.reviews.models import ReviewRequest, Review
from reviewboard.reviews import signals


class CIAClient(object):
    """
    A client for the CIA servers. Reports information to the server.
    """
    NAME = "Review Board CIA Notifier"
    VERSION = 0.1

    def __init__(self, extension):
        self.extension = extension

        print "Listening"
        signals.published.connect(self._review_request_published,
                                  sender=ReviewRequest)
        signals.published.connect(self._review_published,
                                  sender=Review)
        print "Done setting up"

    def send_message(self, review_request, author, log_message):
        project = self.extension.settings['project']
        module = self.extension.settings['module']
        cia_server = self.extension.settings['server']

        site = Site.objects.get(pk=settings.SITE_ID)
        url = "%s://%s%s" % (settings.DOMAIN_METHOD, site.domain,
                             review_request.get_absolute_url())

        msg  = "<message>"
        msg += " <generator>"
        msg += "  <name>%s</name>" % self.NAME
        msg += "  <version>%s</version>" % self.VERSION
        msg += " </generator>"
        msg += " <source>"
        msg += "  <project>%s</project>" % project
        msg += "  <module>%s</module>" % module
        msg += " </source>"
        msg += " <body>"
        msg += "  <commit>"
        msg += "   <revision>%s</revision>" % review_request.id
        msg += "   <author>%s</author>" % author
        msg += "   <log>%s</log>" % log_message
        msg += "   <url>%s</url>" % url
        # TODO: Files?
        msg += "  </commit>"
        msg += " </body>"
        msg += "</message>"

        print msg
        xmlrpclib.ServerProxy(cia_server).hub.deliver(msg)

    def _review_request_published(self, instance, **kwargs):
        print "_review_request_published: %s" % instance
        if instance:
            self.send_message(instance, instance.submitter, instance.summary)

    def _review_published(self, instance, **kwargs):
        print "_review_published: %s" % instance
        if instance:
            self.send_message(instance.review_request, instance.user,
                              instance.body_top)
