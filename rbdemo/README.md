Demo Server Extension
=====================

Overview
--------

This extension manages the server at http://demo.reviewboard.org/.

**Note:** This won't be useful for most people, but could be an interesting
read for those working on writing an extension, particularly ones providing an
authentication backend.

Most of the functionality has to do with account management. When a user
goes to the Log In page, they will be given a generated username and
password they can use to log in. Entering that username and password will
cause an account to be generated, which they can use to test without much
risk of another user using the system.

This also handles resetting the state of the demo server periodically,
through a `reset-demo` management command.


Requirements
-------------

This extension requires Review Board 2.0 RC 1 or higher.


Status
------

This extension is production-ready, but not really useful for any real
installations but ours.
