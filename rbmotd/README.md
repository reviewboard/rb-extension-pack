Message of the Day for Review Board
===================================

[![Review Board 7](https://img.shields.io/badge/7.x-d0e6ff?label=Review%20Board)](https://www.reviewboard.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

The Message of the Day extension for
[Review Board](https://www.reviewboard.org/) helps administrators communicate
important updates to users on the server. This can be used to announce upcoming
downtime, maintenance, an details on a new upgrade.

Messages are shown at the top of the page and may include basic HTML
formatting, including links to more detailed notices.

Users can dismiss a message they've already seen if they no longer want to
see it.


Requirements
============

This requires [Review Board 7](https://www.reviewboard.org/) or higher.


Installation
============

Installation is easy. Just follow these steps:

1. Install the extension:

   ```shell
   $ rb-site manage /path/to/sitedir pip install rbmotd
   ```

2. Log into Review Board as an administrator.

3. Visit **Admin UI -> Extensions** and click **Reload Extensions**

4. Click **Enable** next to the extension.

5. To configure a message, click **Configure**.


Getting Support
===============

We can help you get going with Review Board and the Message of the Day
extension, and diagnose any issues that may come up.

We provide more [dedicated, private
support](https://www.reviewboard.org/support/) for your organization through a
support contract, offering:

* Same-day responses (generally within a few hours, if not sooner)
* Confidential communications
* Installation/upgrade assistance
* Emergency database repair
* Video/chat meetings (by appointment)
* Priority fixes for urgent bugs
* Backports of urgent fixes to older releases (when possible)
