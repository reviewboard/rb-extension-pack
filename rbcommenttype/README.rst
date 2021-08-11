===================================
Review Board Comment Categorization
===================================

This is an extension to `Review Board`_ that adds a new field when writing
comments, allowing users to choose a category (such as security, performance,
bug fixes, etc.) for a comment. This can help teams prioritize the type of
feedback they give and address.


.. _Review Board: https://www.reviewboard.org


Requirements
============

The comment categorization extension requires Review Board 3.0 or newer.


Installation
============

To install this extension, run::

    sudo pip install -U rbcommenttype

If you're on Python 2.7 and previously installed using
``easy_install``, run::

    sudo easy_install -U rbcommenttype


Once done, log in to Review Board's administration interface. Navigate to
**Extensions**, select **Comment Categorization**, and click **Enable**.

If you don't see this extension, reload/rescan your list of extensions.


Configuration
=============

The available categories are set in the extension's administration interface.
From the extension list in the Review Board administration UI, click
**Configure** to get to the extension configuration.

If you want users to have to specify a comment type for every comment that they
file, select **Require comment type**. If this is not selected, users can leave
the field blank when making new comments.

Below this is a table of the available type names. New types can be added by
clicking **Add type**.

Types can be removed by clicking the **X** to the right of the name, or hidden
by un-checking the "Visible" check-box.

Once changes have been made, click **Save** to update the configuration.


Usage
=====

When creating a new comment, the comment dialog will contain a new **Type**
drop-down with the configured type names.

The comment type saved with each comment can be seen next to the comment text,
and is also available in the API (in the ``extra_data.commentType`` key in the
various comment resources).


Contributing
============

Are you a developer? Do you want to help improve this extension? Great! Let's
help you get started.

First off, read through our `contributor guide`_.

We accept patches to Review Board-related projects on
https://reviews.reviewboard.org. (Please note that we do not accept pull
requests on GitHub.)

Got any questions about anything related to RBTools and development? Head
on over to our `development discussion list`_.


.. _contributor guide:
   https://www.notion.so/reviewboard/Review-Board-45d228fb07a0459b84fee509ac054cec).
.. _development discussion list:
   https://groups.google.com/group/reviewboard-dev/.
