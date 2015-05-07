from __future__ import unicode_literals

from djblets.webapi.resources import (register_resource_for_model,
                                      unregister_resource_for_model)
from reviewboard.accounts.forms.pages import AccountPageForm
from reviewboard.accounts.pages import AccountPage
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import (AccountPagesHook,
                                          TemplateHook)
from reviewboard.urls import reviewable_url_names

from checklist.resources import (checklist_item_resource, checklist_resource,
                                 checklist_template_resource)
from checklist.models import ChecklistTemplate, ReviewChecklist


class ChecklistAccountPageForm(AccountPageForm):
    form_id = 'checklist_accountpage_form'
    form_title = 'Manage Checklist Templates'
    save_label = None

    js_view_class = 'RB.ChecklistAccountPageView'


class ChecklistAccountPage(AccountPage):
    page_id = 'checklist_accountpage'
    page_title = 'Checklist Templates'
    form_classes = [ChecklistAccountPageForm]


class Checklist(Extension):
    metadata = {
        'Name': 'Review Checklist',
    }

    js_model_class = 'Checklist.Extension'

    css_bundles = {
        'css_default': {
            'source_filenames': ['css/style.less'],
            'apply_to': reviewable_url_names,
        },
        'accountpage': {
            'source_filenames': ['css/accountpage.less'],
            'apply_to': 'user-preferences',
        },
    }

    js_bundles = {
        'js_default': {
            'source_filenames': ['js/models/checklist.js',
                                 'js/models/checklistAPI.js',
                                 'js/views/checklistView.js'],
        },
        'accountpage': {
            'source_filenames': ['js/models/checklist.js',
                                 'js/models/checklistTemplate.js',
                                 'js/views/checklistAccountPageView.js'],
            'apply_to': 'user-preferences',
        },
    }

    resources = [checklist_resource, checklist_item_resource,
                 checklist_template_resource]

    def __init__(self, *args, **kwargs):
        super(Checklist, self).__init__(*args, **kwargs)

        register_resource_for_model(ReviewChecklist, checklist_resource)
        register_resource_for_model(ChecklistTemplate,
                                    checklist_template_resource)

        TemplateHook(self, 'base-scripts-post', 'checklist/template.html',
                     apply_to=reviewable_url_names)

        AccountPagesHook(self, [ChecklistAccountPage])

    def shutdown(self, *args, **kwargs):
        super(Checklist, self).shutdown(*args, **kwargs)

        unregister_resource_for_model(ReviewChecklist)
        unregister_resource_for_model(ChecklistTemplate)
