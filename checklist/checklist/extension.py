# Checklist Extension for Review Board.
from djblets.webapi.resources import (register_resource_for_model,
                                        unregister_resource_for_model)
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import TemplateHook

from checklist.checklistResource import checklist_resource
from checklist.models import ReviewChecklist


class Checklist(Extension):
    metadata = {
        'Name': 'Review Checklist',
    }

    js_model_class = 'Checklist.Extension'

    css_bundles = {
        'css_default': {
            'source_filenames': ['css/index.css']
        }
    }

    js_bundles = {
        'js_default': {
            'source_filenames': ['js/models/checklist.js',
                                 'js/models/checklistAPI.js',
                                 'js/views/checklistView.js']
        }
    }

    resources = [checklist_resource]

    def __init__(self, *args, **kwargs):
        super(Checklist, self).__init__(*args, **kwargs)
        register_resource_for_model(ReviewChecklist, checklist_resource)
        TemplateHook(self, 'base-scripts-post', 'checklist/template.html',
                     apply_to=['view_diff', 'view_diff_revisions',
                               'file_attachment'])

    def shutdown(self, *args, **kwargs):
        unregister_resource_for_model(ReviewChecklist)
