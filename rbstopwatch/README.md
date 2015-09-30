Review Stopwatch
================

The review stopwatch is an extension which adds a timer to each review request.
Reviewers can start and stop it to keep track of the total time that they've
spent on each review.


Requirements
------------

Review Stopwatch requires Review Board 2.0.17 or newer.


Installation
------------

To install Review Stopwatch, just run this command (as root):

    easy_install rbstopwatch

Once done, log in to Review Board's administration interface and select
"Extensions" at the top of the page. If you don't see the "Review Stopwatch"
extension, click "Scan for installed extensions". Click "Enable" on the
extension, and everything should be set up.


Using the stopwatch
-------------------

The stopwatch can be seen at the bottom-right of all review request pages (such
as the review request, diff viewer, and file attachment pages). Clicking on the
stopwatch will start it, and clicking again will stop it and save the current
time.

Note that if you have multiple browser tabs or windows open for the same review
request (such as one looking at the diff view and another at a file
attachment), you cannot run multiple stopwatches at the same time. Whichever
one is stopped last will save its value. If you do run with multiple tabs, we
suggest keeping your timer running in only one of them, or stopping and
starting them each time you navigate to a different page.

The total time spent on each review can be seen in the review box just above
the comments, and is also available in the API (the
`extra_data.rbstopwatch.reviewTime` key in the review resource contains the
total number of seconds spent on the review).
