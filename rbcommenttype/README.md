Review Board Comment Categorization
===================================

This extension adds a new field to comments which allows users to categorize
them into types.


Requirements
------------

The comment categorization extension requires Review Board 2.0.18 or newer.


Installation
------------

To install this extension, just run this command (as root):

    easy_install rbcommenttype


Once done, log in to Review Board's administration interface and select
"Extensions" at the top of the page. If you don't see the "Comment
Categorization" extension, click "Scan for installed extensions". Click
"Enable" on the extension.


Configuration
-------------

The available categories are set in the extension's administration interface.
From the extension list in the Review Board administration UI, click
"Configure" to get to the extension configuration.

If you want users to have to specify a comment type for every comment that they
file, select "Require comment type". If this is not selected, users can leave
the field blank when making new comments.

Below this is a table of the available type names. New types can be added by
clicking "Add type". Types can be removed by clicking the "X" to the right of
the name, or hidden by un-checking the "Visible" check-box. Once changes have
been made, click "Save" to update the configuration.


Usage
-----

When creating a new comment, the comment dialog will contain a new "Type"
drop-down with the configured type names.

The comment type saved with each comment can be seen next to the comment text,
and is also available in the API (in the `extra_data.commentType` key in the
various comment resources).
