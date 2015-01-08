from reviewboard.extensions.hooks import ReviewRequestDropdownActionHook


class ReviewRequestDropdownActionHookWithDynamicUrl(
        ReviewRequestDropdownActionHook):
    """A hook for adding actions with dynamic urls to the review request page.

    Each url field should be string formatted with %s.
    For example:
        actions = [{
            'id': 'id 0',
            'label': 'Title',
            'items': [
                {
                    'id': 'id 1',
                    'label': 'Item 1',
                    'url': '.../%s...',
                },
            ],
        }]
    """
    def get_actions(self, context):
        """Format the urls to include the Review Request's id."""
        import copy
        actions = copy.deepcopy(self.actions)
        review_request = context.get('review_request')
        for action_dic in actions:
            for dic in action_dic.get('items'):
                dic['url'] = dic['url'] % review_request.display_id
        return actions
