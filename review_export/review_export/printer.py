from io import BytesIO
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.sequencer import Sequencer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (Image, ListFlowable, ListItem, Paragraph,
                                ParagraphAndImage, SimpleDocTemplate)
from reportlab.platypus.flowables import KeepTogether, Spacer
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.reviews.models import Review

from data_extractor import (ChangeDescriptionData, CommentData,
                            FileAttachmentData, ReviewData, ReviewRequestData)


class ReviewRequestPDFPrinter(object):
    BULLET = {
        'type': 'bullet',    # Bullet type
        'symbol': 'circle',  # Symbol for each bullet
        'indent': 40,        # Space to indent each level of bullet points
        'size': 11,          # Size of the bullet symbol
    }

    PARAGRAPH = {
        'spaceAfter': 24,   # Space between dissimilar paragraphs
    }

    LIGHT_GREEN = '#dfffd7'
    LIGHT_RED = '#ffe0e5'
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name='body',
            spaceAfter=PARAGRAPH['spaceAfter']
        )
    )
    comment_style = ParagraphStyle(
        name='Comment',
    )

    COMMENT_FLI = 12    # First Line Indent
    FULL_INDENT = 24
    styles['Normal'].clone(comment_style)
    comment_style.leftIndent = FULL_INDENT           # Indent entire paragraph
    comment_style.firstLineIndent = -COMMENT_FLI     # Counter-act Para indent
    comment_style.spaceAfter = 8            # Spacing after each Paragraph
    comment_style.textColor = colors.gray   # Font Color

    diff_heading_style = ParagraphStyle(
        name='Diff_Heading',
    )
    styles['Normal'].clone(diff_heading_style)
    diff_heading_style.textColor = colors.gray   # Font Color
    # Same column as Comment first line
    diff_heading_style.leftIndent = COMMENT_FLI

    # Style for contents added in the Change Description
    diff_plus_style = ParagraphStyle(
        name='Diff_Plus',
    )
    styles['Normal'].clone(diff_plus_style)
    diff_plus_style.leftIndent = FULL_INDENT         # Indent entire paragraph
    diff_plus_style.backColor = colors.HexColor(LIGHT_GREEN)
    diff_plus_style.textColor = colors.gray   # Font Color

    # Style for contents removed in the Change Description
    diff_minus_style = ParagraphStyle(
        name='Diff_Minus',
    )
    styles['Normal'].clone(diff_minus_style)
    diff_minus_style.leftIndent = FULL_INDENT        # Indent entire paragraph
    diff_minus_style.backColor = colors.HexColor(LIGHT_RED)
    diff_minus_style.textColor = colors.gray   # Font Color

    styles.add(comment_style)
    styles.add(diff_heading_style)
    styles.add(diff_plus_style)
    styles.add(diff_minus_style)

    def __init__(self, review_request, pagesize):
        self.buffer = BytesIO()
        self.review_request = review_request
        self.rr_handler = ReviewRequestData(review_request)
        self.comment_handler = CommentData()

        # Work around for providing review request id to NumberedCanvas
        NumberedCanvas.review_request_id = review_request.id

        # Container holding 'Flowable' objects (objects written to document)
        self.elements = []
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
        self.doc = SimpleDocTemplate(self.buffer,
                                     rightMargin=72,
                                     leftMargin=72,
                                     topMargin=72,
                                     bottomMargin=72,
                                     pagesize=self.pagesize)

    def generate_report(self):
        # Ordering Format for document/report
        self.print_title()

        self.print_description()

        self.print_testing_done()

        self.print_details()

        self.print_issue_summary()

        self.print_file_summary()

        self.print_review_summary()

        # Build document
        self.doc.build(self.elements, canvasmaker=NumberedCanvas)
        document = self.buffer.getvalue()
        self.buffer.close()
        return document

    def print_title(self):
        """Print title at the top of the document.

        The format is:
         --------------
        |    Review    |Review Request Summary
        |    Board     |Review Request Submitter
        |    Logo      |Review Request Status
         --------------
        """
        e = []
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'rblogo.png')
        img = Image(img_path)
        img.drawHeight = 1 * inch * img.drawHeight / img.drawWidth
        img.drawWidth = 1 * inch
        e = []
        e.append('%s' % (self.rr_handler.get_summary()))
        e.append('<br />')
        e.append('<b>%s: </b>%s' % ('Submitter',
                                    str(self.rr_handler.get_submitter())))
        e.append('<br />')
        e.append('<b>%s: </b>%s' % ('Status', self.rr_handler.get_status()))
        para = Paragraph(''.join(e), self.styles['body'])
        self.elements.append(ParagraphAndImage(para, img, side='left'))

    def print_description(self):
        e = []
        e.append(Paragraph(
                 'Description', self.styles['Heading1']))
        e.append(Paragraph(
                 self.rr_handler.get_description(), self.styles['body']))
        self.elements.append(KeepTogether(e))

    def print_testing_done(self):
        e = []
        e.append(Paragraph(
                 'Testing Done',
                 self.styles['Heading1']))
        e.append(Paragraph(
                 self.rr_handler.get_testing_done(),
                 self.styles['body']))
        self.elements.append(KeepTogether(e))

    def print_details(self):
        self.elements.append(Paragraph(
                             'Details',
                             self.styles['Heading2']))

        self.elements.append(Paragraph(
            '<b>Date Created:</b> %s' % self.rr_handler.get_date_created(),
            self.styles['Normal']))

        self.elements.append(Paragraph(
            '<b>Date Updated:</b> %s' % self.rr_handler.get_date_updated(),
            self.styles['Normal']))

        self.elements.append(Paragraph(
            '<b>Repository:</b> %s' % self.rr_handler.get_repository(),
            self.styles['Normal']))

        self.elements.append(Paragraph(
            '<b>Branch:</b> %s' % self.rr_handler.get_branch(),
            self.styles['Normal']))

        bugs = self.rr_handler.get_bugs()
        if bugs:
            # Contains bug list
            e = []
            e.append(Paragraph(
                     '<b>Bugs:</b>',
                     self.styles['Normal']))
            e.append(self._create_list(bugs))
            self.elements.append(KeepTogether(e))

        dependencies = self.rr_handler.get_dependencies()
        if dependencies:
            e = []
            e.append(Paragraph(
                     '<b>Depends On:</b>',
                     self.styles['Normal']))
            e.append(self._create_list(dependencies))
            self.elements.append(KeepTogether(e))

        reviewers = self.rr_handler.get_reviewers()
        if reviewers:
            e = []
            e.append(Paragraph(
                     '<b>Reviewers:</b>',
                     self.styles['Normal']))
            e.append(self._create_list(reviewers))
            self.elements.append(KeepTogether(e))
            self.print_element_spacer()

    def print_issue_summary(self):
        """Adds an issue summary section to the PDF.

        Retrieves, constructs, and prints the information associated with
        the review request's issues
        """

        def create_comment_list(comments):
            """Creates a ListFlowable of comments.

            All comments should be of the same issue status
            """
            list_items = []
            seq = Sequencer()
            for comment in comments:
                self.comment_handler.set_comment(comment)
                list_items.append(
                    ListItem(
                        Paragraph(
                            "%s - %s" % (
                                self.comment_handler.get_user_full_name(),
                                comment),
                            self.styles['Normal']),
                        leftIndent=self.BULLET['indent'],
                        bulletFontSize=self.BULLET['size'],
                        value='%d.' % seq.next('comment'),
                        alignment=TA_CENTER))
            return ListFlowable(
                list_items,
                bulletType=self.BULLET['type'])

        self.elements.append(Paragraph(
                             '<b>Issue Summary (%d)</b>' %
                             self.rr_handler.get_num_issues(),
                             self.styles['Heading1']))

        # Generate dictionary to organize comments by status
        issues = self.rr_handler.get_issues_by_status()

        # Display issues by status
        for status in issues:
            e = []
            if issues[status]:
                # Only display issues of 'status' if non-empty
                self.comment_handler.set_comment(issues[status][0])
                status_string = self.comment_handler.get_issue_status()
                issue_count = self.rr_handler.get_num_issues(
                    [status_string.lower()])
                e.append(Paragraph(
                         '%s (%d)' % (status_string, issue_count),
                         self.styles['Heading2']))
                e.append(create_comment_list(issues[status]))
                self.elements.append(KeepTogether(e))
                self.print_element_spacer()

    def print_file_summary(self):
        """Adds a File Summary section to the PDF.

        Retrieves, constructs, and prints the information associated with
        the files uploaded to the review request
        """
        def create_attachment_list(file_attachments):
            """Creates a ListFlowable of file attachments."""
            fa_handler = FileAttachmentData()
            list_items = []
            seq = Sequencer()
            for attachment in file_attachments:
                fa_handler.set_file_attachment(attachment)
                list_items.append(
                    ListItem(
                        Paragraph(
                            '%s: %s' %
                            (fa_handler.get_filename(),
                             fa_handler.get_caption()),
                            self.styles['Normal']),
                        leftIndent=self.BULLET['indent'],
                        bulletFontSize=self.BULLET['size'],
                        value='%d.' % seq.next('file_attachments'),
                        alignment=TA_CENTER))
            return ListFlowable(
                list_items,
                bulletType=self.BULLET['type'])

        file_attachments = self.rr_handler.get_file_attachments()
        inactive_file_attachments = \
            self.rr_handler.get_inactive_file_attachments()

        total_file_attachments = len(file_attachments) + \
            len(inactive_file_attachments)

        # Only display File Summary section if there is at least one file
        # uploaded or deleted from the review request
        if total_file_attachments > 0:
            self.elements.append(Paragraph(
                '<b>File Summary (%d)</b>' % total_file_attachments,
                                 self.styles['Heading1']))
            if len(file_attachments) > 0:
                self.elements.append(Paragraph(
                    '<b>Uploaded (%d)</b>' % len(file_attachments),
                                     self.styles['Heading2']))
                self.elements.append(create_attachment_list(
                                     file_attachments))
            if len(inactive_file_attachments) > 0:
                self.elements.append(Paragraph(
                    '<b>Deleted (%d)</b>' % len(inactive_file_attachments),
                                     self.styles['Heading2']))
                self.elements.append(create_attachment_list(
                                     inactive_file_attachments))

        self.print_element_spacer()

    def print_changeset_summary(self):
        """Adds a Change Set Summary section to the PDF.

        Retrieves and prints the changes made to the modified files
        in the implementation of the review request
        """
        def create_change_list(change_list):
            """Creates a ListFlowable of reviews."""
            list_items = []
            seq = Sequencer()
            for change in change_list:
                list_items.append(
                    ListItem(
                        Paragraph(
                            '<b>%s: %s</b>' %
                            ('review type', 'by person'),
                            self.styles['Normal']),
                        leftIndent=self.BULLET['indent'],
                        bulletFontSize=self.BULLET['size'],
                        value='%d.' % seq.next('reviews'),
                        alignment=TA_CENTER))
            return ListFlowable(
                list_items,
                bulletType=self.BULLET['type'])

        self.elements.append(Paragraph(
            '<b>Change Set Summary</b>',
            self.styles['Heading1']))

        num_revisions = 0
        self.elements.append(Paragraph(
            '<b>Number of Revisions: %d</b>' % num_revisions,
            self.styles['Normal']))

        num_files = 0
        self.elements.append(Paragraph(
            '<b>Number of Files: %d</b>' % num_files,
            self.styles['Normal']))

    def print_review_summary(self):
        """Adds a Review Summary section to the PDF.

        Retrieves and prints the reviews of the review request
        """
        def create_review_list(reviews):
            """Creates a ListFlowable of reviews and Change Descriptions."""
            def generate_change_request(change_request):
                """Creates a list of Flowable objects for a Change Request."""

                def change_description_content(key, fields):
                    """Creates the list of paragraph elements for the specified
                    key and dictionary."""
                    cd_handler = ChangeDescriptionData(change_request)
                    changes = cd_handler.get_changes(key)

                    content = []
                    if changes:
                        content.append(Paragraph(
                            '%s:' % changes.get('title'),
                            self.styles['Diff_Heading']))
                        for element in changes.get('removed'):
                            # Content was removed from the field
                            content.append(Paragraph(
                                '- %s' % element,
                                self.styles['Diff_Minus']))
                        for element in changes.get('added'):
                            # Content was added to the field
                            content.append(Paragraph(
                                '+ %s' % element,
                                self.styles['Diff_Plus']))
                    return content

                e = []
                e.append(Paragraph(
                    '<b>%s</b>' % 'Review Request Changed',
                    self.styles['Normal']))

                e.append(Paragraph(
                    '<b>Change Summary:</b> %s' % str(change_request.text),
                    self.styles['Comment']))

                modified_fields = change_request.fields_changed
                for key, fields in modified_fields.iteritems():
                    summary = change_description_content(key, fields)
                    for para in summary:
                        e.append(para)
                return e

            def generate_review(review):
                """Creates a list of Flowable objects for the Review."""
                review_handler = ReviewData(review)
                e = []
                # Each review has its main comment when first published
                # If the review references a Diff or File
                main_comment = review_handler.get_all_comments()
                if main_comment:
                    main_comment = main_comment[0]  # Review's initial text

                if main_comment and main_comment.issue_opened:
                    self.comment_handler.set_comment(main_comment)
                    title = 'Issue Opened by %s (%s)' % (
                        self.comment_handler.get_user_full_name(),
                        self.comment_handler.get_issue_status().capitalize())
                else:
                    title = 'Review by %s' % (
                        review_handler.get_user_full_name())

                e.append(Paragraph(
                    '<b>%s</b>' % title,
                    self.styles['Normal']))

                # same procedure for top,comment,bottoms
                # fix spacing. maybe add some background colour for each reply
                if review.body_top:
                    body_top_list = review_handler.get_body_top_replies()
                    body_top_list.insert(0, review)  # Add this review as first
                    r_handler = ReviewData()
                    for reply in body_top_list:
                        r_handler.set_review(reply)
                        e.append(Paragraph(
                            '%s:<br/>%s' % (r_handler.get_user_full_name(),
                                            r_handler.get_body_top()),
                            self.styles['Comment']))

                if main_comment:
                    self.comment_handler.set_comment(main_comment)
                    comment_list = list(self.comment_handler.get_replies())
                    comment_list.insert(0, main_comment)
                    for reply in comment_list:
                        self.comment_handler.set_comment(reply)
                        e.append(Paragraph(
                            '%s:<br/>%s' % (
                                self.comment_handler.get_user_full_name(),
                                str(self.comment_handler.get_text())),
                            self.styles['Comment']))

                if review.body_bottom:
                    body_bottom_list = \
                        review_handler.public_body_bottom_replies()
                    body_bottom_list.insert(0, review)
                    r_handler = ReviewData()
                    for reply in body_bottom_list:
                        r_handler.set_review(reply)
                        e.append(Paragraph(
                            '%s:<br/>%s' % (r_handler.get_user_full_name(),
                                            reply.body_top),
                            self.styles['Comment']))
                return e

            list_items = []
            seq = Sequencer()
            for review in reviews:
                fields = []
                # Don't like the use of isinstance but is there is another way?
                if isinstance(review, ChangeDescription):
                    fields = generate_change_request(review)
                elif isinstance(review, Review):
                    fields = generate_review(review)

                if fields:
                    list_items.append(
                        ListItem(
                            fields,
                            leftIndent=self.BULLET['indent'],
                            bulletFontSize=self.BULLET['size'],
                            value='%d.' % seq.next('reviews'),
                            alignment=TA_CENTER))

            return ListFlowable(
                list_items,
                bulletType=self.BULLET['type'])

        reviews = self.rr_handler.get_review_section()

        if len(reviews) > 0:
            self.elements.append(Paragraph(
                '<b>Review Summary (%d)</b>' % len(reviews),
                self.styles['Heading1']))
            # Sort all reviews and review requests by timestamp
            self.elements.append(create_review_list(reviews))

    def print_element_spacer(self):
        self.elements.append(Spacer(1, self.PARAGRAPH['spaceAfter']))

    def _create_list(self, array):
        list_items = []
        for element in array:
            list_items.append(
                ListItem(
                    Paragraph(
                        str(element),
                        self.styles['Normal']),
                    leftIndent=self.BULLET['indent'],
                    bulletFontSize=self.BULLET['size'],
                    alignment=TA_CENTER))
        return ListFlowable(
            list_items,
            bulletType=self.BULLET['type'],
            start=self.BULLET['symbol'])


class NumberedCanvas(canvas.Canvas):
    """This class adds a 'Page X of Y' Header to the generated PDF document."""
    review_request_id = None

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.width, self.height = letter

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        # Add Page X of Y to each page's header
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages, state['_pagesize'])
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count, pagesize):
        """Add the page number information to the header (right side)."""
        width, height = pagesize
        self.setFont("Helvetica", 10)
        self.drawRightString(width - 20, height - 20,
                             'Review Request %d - Page %d of %d'
                             % (self.review_request_id, self._pageNumber,
                                page_count))


class XMLPrinter(object):
    _COMMONS = \
        {
            'user': ('user_full_name', {'tag_name': 'User'}),
        }
    CHAR_ENCODING = 'UTF-8'
    XML_VERSION = 1.0
    CHAR_MAPPINGS = \
        {
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            "'": '&apos;',
            '"': '&quot;',
        }
    TAGS = \
        {
            'review_request': {
                'tag_name': 'Review-Request',
                'attributes': {
                    'id': 'pk',
                },
                'fields': {
                    'status': {
                        'tag_name': 'status',
                    },
                    'submitter': {
                        'tag_name': 'submitter',
                    },
                    'summary': {
                        'tag_name': 'summary',
                    },
                    'description': {
                        'tag_name': 'description',
                    },
                    'testing_done': {
                        'tag_name': 'testing done',
                    },
                },
            },
            'review': {
                'tag_name': 'Review',
                'attributes': {},
                'fields': {
                    _COMMONS['user'][0]: _COMMONS['user'][1],
                },
                'body_top': {
                    'tag_name': 'Body Top',
                    'fields': {
                        _COMMONS['user'][0]: _COMMONS['user'][1],
                        'body_top': {
                            'tag_name': 'Text',
                        },
                    },
                    'reply': {
                        'tag_name': 'Reply-Top',
                        'attributes': {},
                        'fields': {
                            _COMMONS['user'][0]: _COMMONS['user'][1],
                            'body_top': {
                                'tag_name': 'Text',
                            },
                        },
                    },
                },
                'body_bottom': {
                    'tag_name': 'Reply-Bottom',
                    'fields': {
                        _COMMONS['user'][0]: _COMMONS['user'][1],
                        'body_bottom': {
                            'tag_name': 'Text',
                        },
                    },
                    'reply': {
                        'tag_name': 'Reply',
                        'attributes': {},
                        'fields': {
                            _COMMONS['user'][0]: _COMMONS['user'][1],
                            'body_bottom': {
                                'tag_name': 'Text',
                            },
                        },
                    },
                },
                'comment': {
                    'tag_name': 'Comment',
                    'fields': {
                        _COMMONS['user'][0]: _COMMONS['user'][1],
                        'text': {
                            'tag_name': 'Text',
                        },
                    },
                    'reply': {
                        'tag_name': 'Reply',
                        'attributes': {},
                        'fields': {
                            _COMMONS['user'][0]: _COMMONS['user'][1],
                            'text': {
                                'tag_name': 'Text',
                            },
                        },
                    },
                },
            },
            'change_description': {
                'tag_name': 'Change Description',
                'attributes': {},
                'fields': {
                    'text': {
                        'tag_name': 'Text',
                    },
                },
            },
        }

    LINE_SEP = os.linesep
    TAB_CHAR = '\t'

    def __init__(self, review_request):
        self.buffer = BytesIO()
        self.review_request = review_request
        self.rr_handler = ReviewRequestData(review_request)
        self.comment_handler = CommentData()
        self.tabs = 0

    def set_tabs(self, tabs):
        self.tabs = tabs

    def get_tabs(self):
        return self.tabs

    def increment_tabs(self):
        self.tabs += 1

    def decrement_tabs(self):
        self.tabs -= 1

    def writeline(self, line, ismarkup=False):
        self.writelines([line], ismarkup)

    def writelines(self, lines, ismarkup=False):
        tabs = self.get_tabs()
        tabbed_lines = []   # Make all lines start at the same left-indentation
        for line in lines:
            for newline in line.splitlines():
                string = '%s%s%s' % (self.TAB_CHAR * tabs,
                                     str(newline), self.LINE_SEP)
                if not ismarkup:
                    string = self.xml_escape(string)
                tabbed_lines.append(string.encode(encoding=self.CHAR_ENCODING))
        self.buffer.writelines(tabbed_lines)

    @classmethod
    def xml_escape(cls, string):
        for original, escaped in cls.CHAR_MAPPINGS.iteritems():
            string.replace(original, escaped)
        return string

    def print_xml_heading(self):
        header = '<?xml version="%d" encoding="%s"?>' % (
            self.XML_VERSION,
            self.CHAR_ENCODING)
        self.writeline(header, True)

    def generate_report(self):
        self.print_xml_heading()
        rr_attr = self.TAGS.get('review_request')

        self.print_object(self.rr_handler, rr_attr)
        self.increment_tabs()

        # Print all reviews (sorted by timestamp)
        r_handler = ReviewData()
        cd_handler = ChangeDescriptionData()
        for review in self.rr_handler.get_review_section():
            if isinstance(review, Review):
                attr = self.get_tag('review')
                r_handler.set_review(review)
                self.print_object(r_handler, attr)

                # Write Body Top Info
                self.increment_tabs()
                body_top_attr = attr.get('body_top')
                reply_attr = body_top_attr.get('reply')
                self.print_object(r_handler, body_top_attr)
                for reply in r_handler.get_body_top_replies():
                    self.increment_tabs()
                    r_handler.set_review(reply)
                    self.print_object(r_handler, reply_attr)
                    self.write_ending_tag(reply_attr)
                    self.decrement_tabs()
                self.write_ending_tag(body_top_attr)
                self.decrement_tabs()

                # Write Body Bottom Info
                self.increment_tabs()
                body_bot_attr = attr.get('body_bottom')
                reply_attr = body_top_attr.get('reply')
                self.print_object(r_handler, body_bot_attr)
                self.increment_tabs()
                for reply in r_handler.get_body_bottom_replies():
                    r_handler.set_review(reply)
                    self.print_object(r_handler, reply_attr)
                    self.write_ending_tag(reply_attr)
                self.decrement_tabs()
                self.write_ending_tag(body_bot_attr)
                self.decrement_tabs()

                # Write Comments Info
                comment_attr = attr.get('comment')
                reply_attr = comment_attr.get('reply')
                c_handler = CommentData()
                self.increment_tabs()
                for comment in review.get_all_comments():
                    c_handler.set_comment(comment)
                    self.print_object(c_handler, comment_attr)
                    self.increment_tabs()
                    for reply in c_handler.get_replies():
                        c_handler.set_comment(reply)
                        self.print_object(c_handler, reply_attr)
                        self.write_ending_tag(reply_attr)
                    self.decrement_tabs()
                    self.write_ending_tag(comment_attr)
                self.decrement_tabs()

            elif isinstance(review, ChangeDescription):
                attr = self.get_tag('change_description')
                cd_handler.set_change_description(review)
                self.print_object(cd_handler, attr)
                self.increment_tabs()
                for change in cd_handler.get_fields_changed():
                    self.write_open_tag(change.capitalize())
                    changes = cd_handler.get_changes_added(change)
                    if changes:
                        self.increment_tabs()
                        self.write_open_tag('Added')
                        self.increment_tabs()
                        self.writelines(changes)
                        self.decrement_tabs()
                        self.write_closed_tag('Added')
                        self.decrement_tabs()
                    changes = cd_handler.get_changes_removed(change)
                    if changes:
                        self.increment_tabs()
                        self.write_open_tag('Removed')
                        self.increment_tabs()
                        self.writelines(changes)
                        self.decrement_tabs()
                        self.write_closed_tag('Removed')
                        self.decrement_tabs()
                    self.write_closed_tag(change.capitalize())
                self.decrement_tabs()

            self.write_ending_tag(attr)

        self.decrement_tabs()
        self.write_ending_tag(rr_attr)
        content = self.buffer.getvalue()
        self.buffer.close()
        return content

    def print_object(self, handler, attributes):
        self.write_initial_tag(handler, attributes)
        self.increment_tabs()
        dic = self.get_tag_fields(attributes)
        if dic:
            for (field, field_attr) in dic.iteritems():
                method_value = self.get_function_value(handler,
                                                       'get_%s' % field)
                if method_value:
                    self.write_initial_tag(handler, field_attr)
                    self.increment_tabs()
                    self.writeline('%s' % method_value)
                    self.decrement_tabs()
                    self.write_ending_tag(field_attr)

        self.decrement_tabs()

    @classmethod
    def get_function_value(cls, obj, function_name):
        try:
            method_to_call = getattr(obj, function_name)
            method_value = method_to_call()
            return method_value
        except AttributeError:
            cls.log_error('Function %s does not exist in %s' % (
                function_name, obj.__class__.__name__))
        return None

    @staticmethod
    def log_error(string):
        """Logs the error message instead of throwing an exception."""
        # print 'ERROR: %s' % string
        pass

    def write_open_tag(self, string):
        self.writeline('<%s>' % string, True)

    def write_closed_tag(self, string):
        self.writeline('</%s>' % string, True)

    def write_initial_tag(self, handler, attributes):
        tag = self.get_tag_name(attributes)
        strings = ['<%s' % tag]
        attr_tuples = self.get_tag_attributes(attributes)
        if attr_tuples:
            for (attr_name, attr_method) in attr_tuples.iteritems():
                method_value = self.get_function_value(handler,
                                                       'get_%s' % attr_method)
                if method_value:
                    strings.append(' %s=%s' % (attr_name, method_value))
        strings.append('>')  # Close tag
        self.writeline(''.join(strings), True)    # Write <TAG>

    def write_ending_tag(self, attributes):
        self.writeline('</%s>' % self.get_tag_name(attributes), True)

    def get_tag(self, key=None):
        if key:
            return self.TAGS.get(key)
        else:
            return self.TAGS

    def get_tag_name(self, dic):
        return dic.get('tag_name')

    def get_tag_attributes(self, dic):
        return dic.get('attributes')

    def get_tag_fields(self, dic):
        return dic.get('fields')

    def get_tag_complex_objects(self, dic):
        return dic.get('complex_objects')
