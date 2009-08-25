from django import forms
from django.utils.translation import ugettext as _
from djblets.extensions.forms import SettingsForm


class CIASettingsForm(SettingsForm):
    server = forms.URLField(initial="http://www.cia.vc",
                            help_text=_("The CIA server to send updates to."))
    project = forms.CharField(max_length=64,
                              help_text=_("The project name to use."))
    module = forms.CharField(max_length=64, initial="reviews",
                             help_text=_('The module name to use. '
                                         'Defaults to "reviews".'))
    notify_on_review_requests = forms.BooleanField(
        initial=True, required=False,
        help_text=_("Indicates if CIA should be notified when new review "
                    "requests are published."))

    notify_on_reviews = forms.BooleanField(
        initial=True, required=False,
        help_text=_("Indicates if CIA should be notified when new reviews "
                    "are published."))
