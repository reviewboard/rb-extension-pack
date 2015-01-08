from reviewboard.reviews.models import BaseComment
from reviewboard.webapi.encoder import status_to_string


class ReviewRequestData(object):
    """Extracts information from the Review Board's Review Request model.

    This class encapsulates the details of how to properly extract information
    from Review Board's Review Request object through instance methods. Any
    desired Review Request information should be retrieved from this class.
    """
    DATE_TIME = '%B %d %Y %M %H %S'

    def __init__(self, review_request):
        self.review_request = review_request

    def get_pk(self):
        return self.review_request.pk

    def get_summary(self):
        return str(self.review_request.summary)

    def get_submitter(self):
        user_handler = UserData(self.review_request.submitter)
        return user_handler.get_full_name()

    def get_status(self):
        return str(self.review_request.get_status_display())

    def get_description(self):
        return str(self.review_request.description) or 'None'

    def get_testing_done(self):
        return str(self.review_request.testing_done) or 'None'

    def get_date_created(self):
        return self.review_request.time_added.strftime(self.DATE_TIME)

    def get_date_updated(self):
        return self.review_request.last_updated.strftime(self.DATE_TIME)

    def get_repository(self):
        return str(self.review_request.repository)

    def get_branch(self):
        return str(self.review_request.branch)

    def get_bugs(self):
        SEPARATOR = ","
        bugs = self.review_request.bugs_closed.split(SEPARATOR)
        return [bug.strip() for bug in bugs]

    def get_dependencies(self):
        return self.review_request.depends_on.all()

    def get_target_people(self):
        return list(self.review_request.target_people.all())

    def get_target_groups(self):
        return list(self.review_request.target_groups.all())

    def get_reviewers(self):
        return self.get_target_people() + self.get_target_groups()

    def get_num_issues(self, issue_types=['open', 'resolved', 'dropped']):
        total = 0
        for itype in issue_types:
            total += getattr(self.review_request, 'issue_%s_count' % itype)
        return total

    def get_issues_by_status(self):
        issues = dict((status[0], []) for status in BaseComment.ISSUE_STATUSES)

        review_data = ReviewData()
        comment_data = CommentData()
        for review in self.review_request.reviews.all():
            review_data.set_review(review)
            for comment in review_data.get_all_comments():
                comment_data.set_comment(comment)
                if comment_data.is_issue():
                    issues.get(comment_data.get_issue_code()).append(comment)
        return issues

    def get_file_attachments(self):
        return list(self.review_request.file_attachments.all())

    def get_inactive_file_attachments(self):
        return list(self.review_request.inactive_file_attachments.all())

    def get_reviews(self):
        return list(self.review_request.reviews.all())

    def get_changedescs(self):
        return list(self.review_request.changedescs.all())

    def get_review_section(self):
        reviews = list(
            self.review_request.reviews.filter(base_reply_to_id=None)) + \
            list(self.get_changedescs())
        if reviews:
            reviews.sort(key=lambda item: item.timestamp)
        return reviews


class ReviewData(object):
    """Extracts information from the Review Board's Review model.

    This class encapsulates the details of how to properly extract information
    from Review Board's Review object through instance methods. Any desired
    Review information should be retrieved from this class.
    """
    def __init__(self, review=None):
        self.review = review

    def set_review(self, review):
        self.review = review

    def get_all_comments(self):
        return self.review.get_all_comments()

    def get_user(self):
        return self.review.user

    def get_user_full_name(self):
        user_data = UserData(self.get_user())
        return user_data.get_full_name()

    def get_body_top(self):
        return str(self.review.body_top)

    def get_body_top_replies(self):
        return list(self.review.public_body_top_replies())

    def get_body_bottom(self):
        return list(self.review.body_bottom)

    def get_body_bottom_replies(self):
        return list(self.review.public_body_bottom_replies())


class CommentData(object):
    """Extracts information from the Review Board's Comment model.

    This class encapsulates the details of how to properly extract information
    from Review Board's Comment object through instance methods. Any desired
    Comment information should be retrieved from this class.
    """
    def __init__(self, comment=None):
        self.comment = comment

    def set_comment(self, comment):
        self.comment = comment

    def get_issue_code(self):
        return self.comment.issue_status

    def is_issue(self):
        return bool(self.get_issue_code())

    def get_issue_status(self):
        return str(self.comment.get_issue_status_display())

    def get_user(self):
        return self.comment.get_review().user

    def get_user_full_name(self):
        user_data = UserData(self.get_user())
        return user_data.get_full_name()

    def get_text(self):
        return str(self.comment.text)

    def get_replies(self):
        return list(self.comment.public_replies())


class UserData(object):
    """Extracts information from the Review Board's User model.

    This class encapsulates the details of how to properly extract information
    from Review Board's User object through instance methods. Any desired
    User information should be retrieved from this class.
    """
    def __init__(self, user=None):
        self.user = user

    def set_user(self, user):
        self.user = user

    def get_full_name(self):
        """Return the user's full name if it exists,
        otherwise return their username"""
        result = self.user.get_full_name() or self.get_username()
        return str(result)

    def get_username(self):
        return str(self.user.username)


class FileAttachmentData(object):
    """Extracts information from the Review Board's FileAttachment model.

    This class encapsulates the details of how to properly extract information
    from Review Board's FileAttachment object through instance methods. Any
    desired FileAttachment information should be retrieved from this class.
    """
    def __init__(self, file_attachment=None):
        self.file_attachment = file_attachment

    def set_file_attachment(self, file_attachment):
        self.file_attachment = file_attachment

    def get_filename(self):
        return self.file_attachment.filename

    def get_caption(self):
        return self.file_attachment.caption


class ChangeDescriptionData(object):
    """Extracts information from the Review Board's ChangeDescription model.

    This class encapsulates the details of how to properly extract information
    from Review Board's Change Description object through instance methods. Any
    desired Change Description information should be retrieved from this class.
    """
    FIELDS_CHANGED_ATTRIBUTES = \
        {
            'branch':
                {
                    'plus': 'new',
                    'minus': 'old',
                    'title': 'Branch',
                    'method': 'array1D',
                },
            'bugs_closed':
                {
                    'plus': 'added',
                    'minus': 'removed',
                    'title': 'Bugs Closed',
                    'method': 'bugs_closed',
                },
            'depends_on':
                {
                    'plus': '?',
                    'minus': '?',
                    'title': 'Depends On',
                    'method': 'array1D',
                },
            'description':
                {
                    'plus': 'new',
                    'minus': 'old',
                    'title': 'Description',
                    'method': 'array1D',
                },
            'files':
                {
                    'plus': 'added',
                    'minus': 'removed',
                    'title': 'Files',
                    'method': 'file_content',
                },
            'summary':
                {
                    'plus': 'new',
                    'minus': 'old',
                    'title': 'Summary',
                    'method': 'array1D',
                },
            'status':
                {
                    'plus': 'new',
                    'minus': 'old',
                    'title': 'Status',
                    'method': 'status',
                },
            'target_groups':
                {
                    'plus': 'added',
                    'minus': 'removed',
                    'title': 'Target Groups',
                    'method': 'targets',
                },
            'target_people':
                {
                    'plus': 'added',
                    'minus': 'removed',
                    'title': 'Target People',
                    'method': 'targets',
                },
            'testing_done':
                {
                    'plus': 'new',
                    'minus': 'old',
                    'title': 'Testing Done',
                    'method': 'array1D',
                },
        }

    def __init__(self, change_desc=None):
        self.change_description = change_desc

    def set_change_description(self, change_desc):
        self.change_description = change_desc

    def get_text(self):
        return str(self.change_description.text)

    def get_fields_changed(self):
        fields = []
        for field in self.change_description.fields_changed:
            fields.append(str(field))
        return fields

    def get_title(self, field):
        mapping_keys = \
            self.FIELDS_CHANGED_ATTRIBUTES.get(field) or {}
        return mapping_keys.get('title')

    def get_changes(self, field):
        """Returns dictionary of changes made in a Change Description object.

        Return value has the following fields:
            'title': Title of the field
            'added': Array of strings added to the field
            'removed': Array of strins removed from the field
        """
        plus = self.get_changes_added(field)
        minus = self.get_changes_removed(field)

        if plus or minus:
            # As long as some changes exist
            info = {
                'title': self.get_title(field),
                'added': plus,
                'removed': minus,
            }
            return info
        else:
            return None

    def get_changes_added(self, field):
        """Returns a list of strings that were added to the field."""
        mapping_keys = \
            self.FIELDS_CHANGED_ATTRIBUTES.get(field) or {}
        plus = self.change_description.fields_changed.get(field) or {}
        plus = plus.get(mapping_keys.get('plus')) or []
        method_to_call = getattr(self, mapping_keys['method'])
        content = method_to_call(plus)
        return filter(None, content)

    def get_changes_removed(self, field):
        """Returns a list of strings that were removed from the field."""
        mapping_keys = \
            self.FIELDS_CHANGED_ATTRIBUTES.get(field) or {}
        minus = self.change_description.fields_changed.get(field) or {}
        minus = minus.get(mapping_keys.get('minus')) or []
        method_to_call = getattr(self, mapping_keys['method'])
        content = method_to_call(minus)
        return filter(None, content)

    def array1D(self, content):
        """This is a reflector method that returns the specified array.

        The array parameter is trimmed before being returned.
        Use: When a field is an array with proper formatting and we can just
        keep the contents of the array as is and do not need to process it
        further.
        """
        return filter(None, content)

    def bugs_closed(self, content):
        """Format for target people and groups is an array of arrays.

        Content is a 2D array and the inner arrays are of format (bug name).
        Returns a list of strings representing each user/group in content.
        """
        BUG_NAME = 0
        strings = []
        for array in content:
            strings.append(str(array[BUG_NAME]))
        return strings

    def status(self, content):
        """Format for status field is a one-element array.

        Content is a one-element array containing the unicode character
        corresponding to the review request's status display. This converts
        the unicode character to the proper human-readable word.
        """
        return [str(status_to_string(content[0]))]

    def targets(self, content):
        """Format for target people and groups is an array of arrays.

        Content is a 2D array and the inner arrays are of format
        (user/group name, url for user/group, id).
        Returns a list of strings representing each user/group in content.
        """
        USERNAME = 0
        strings = []
        for tuple_info in content:
            username = str(tuple_info[USERNAME])
            strings.append('%s' % username)
        return strings

    def file_content(self, content):
        """Format for file is an array of arrays.

        Content is a 2D array and the inner arrays are of format
        (caption, filepath, id).
        Filepath is separated from filename by __ (2 underscores).
        Returns a list of strings representing each file in content.
        The strings are of format 'filename: caption'.
        """
        SEPARATION = '__'
        CAPTION = 0
        FILEPATH = 1
        strings = []
        for tuple_info in content:
            caption = str(tuple_info[CAPTION])
            filename = tuple_info[FILEPATH].split(SEPARATION)
            filename = str(filename[1])  # Retrieve filename
            strings.append('%s: %s' % (filename, caption))
        return strings
