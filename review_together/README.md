review\_together
================

Review Board is a web-based code review tool that takes the pain out of code review.

[Mozilla Labs' TogetherJS](http://togetherjs.com/) (formerly TowTruck) makes it
easy to let the viewers of a web page chat with one another - either via text,
or over WebRTC with their microphones.

review\_together is an extension for Review Board that lets users chat via
TogetherJS.

## Installation

Clone, this directory onto the machine with your Review Board instance running
on it. Then, run:

    python setup.py install

to do the install.

Finally, log in to Review Board's administrator interface, and choose
"Extensions" at the top of the page. You should see "review-together" listed as
an available extension. Click on "Enable", and you should be all set!

## I installed the extension. Why isn't it working?

Currently, this extension only works with Review Board 1.7.15 and higher. Make
sure your Review Board instance is up to date.

## Setting up your own hub.

By default Review Together runs on a hub hosted by Mozilla but you can run your
own TogetherJS hub. You can download a hub server
[here.](https://github.com/mozilla/togetherjs/blob/develop/hub/server.js) This
will require [NodeJS.](http://nodejs.org/download/)

To run the server, type the following command in the directory where you
downloaded the file:

    node server.js

Make note of the URL and port where your server is running. To point your
Review Board instance to this hub, go to your admin panel. Click on Extensions
and where ReviewTogether is listed amongst other extensions under the "Manage
Extensions" container, click on configure. There an input box for you to paste
the url of your hub. Your hub URL and port make look something like this:

    http://203.0.113.48:8080
