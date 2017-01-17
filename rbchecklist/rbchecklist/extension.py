from __future__ import unicode_literals

from djblets.webapi.resources import (register_resource_for_model,
                                      unregister_resource_for_model)
from reviewboard.accounts.forms.pages import AccountPageForm
from reviewboard.accounts.pages import AccountPage
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import AccountPagesHook
from reviewboard.urls import review_request_url_names

from rbchecklist.resources import (checklist_item_resource,
                                   checklist_resource,
                                   checklist_template_resource)
from rbchecklist.models import ChecklistTemplate, ReviewChecklist


class ChecklistAccountPageForm(AccountPageForm):
    form_id = 'checklist_accountpage_form'
    form_title = 'Manage Checklist Templates'
    save_label = None

    js_view_class = 'Checklist.AccountPageView'


class ChecklistAccountPage(AccountPage):
    page_id = 'checklist_accountpage'
    page_title = 'Checklist Templates'
    form_classes = [ChecklistAccountPageForm]


class Checklist(Extension):
    """The checklist extension."""

    metadata = {
        'Name': 'Review Checklist',
    }

    css_bundles = {
        'checklist': {
            'source_filenames': ['css/style.less'],
            'apply_to': review_request_url_names,
        },
        'accountpage': {
            'source_filenames': ['css/accountpage.less'],
            'apply_to': 'user-preferences',
        },
    }

    js_bundles = {
        'checklist': {
            'source_filenames': [
                'js/checklist.es6.js',
                'js/models/checklistModel.es6.js',
                'js/views/checklistView.es6.js',
            ],
            'apply_to': review_request_url_names,
        },
        'accountpage': {
            'source_filenames': [
                'js/models/checklistModel.es6.js',
                'js/models/checklistTemplateModel.es6.js',
                'js/views/checklistAccountPageView.es6.js',
            ],
            'apply_to': 'user-preferences',
        },
    }

    resources = [checklist_resource, checklist_item_resource,
                 checklist_template_resource]

    def initialize(self):
        """Initialize the extension."""
        register_resource_for_model(ReviewChecklist, checklist_resource)
        register_resource_for_model(ChecklistTemplate,
                                    checklist_template_resource)

        AccountPagesHook(self, [ChecklistAccountPage])

    def shutdown(self):
        """Shut down the extension."""
        super(Checklist, self).shutdown()

        unregister_resource_for_model(ReviewChecklist)
        unregister_resource_for_model(ChecklistTemplate)
