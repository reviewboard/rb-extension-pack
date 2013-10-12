reviewboard_together
====================

Review Board is a web-based code review tool that takes the pain out of code review.

[Mozilla Labs' TogetherJS](http://togetherjs.com/) (formerly TowTruck) makes it easy to let the viewers of a web page
chat with one another - either via text, or over WebRTC with their microphones.

reviewboard_together is an extension for Review Board that lets users chat via TogetherJS.

## Installation

Fork, or [download the contents of this repository](https://github.com/mikeconley/reviewboard_together/archive/master.zip) onto the machine with your Review Board instance running on it. Then, run:

    python setup.py

to do the install.

Finally, log in to Review Board's administrator interface, and choose "Extensions" at the top of the page. You should see "reviewboard-together" listed as an available extension. Click on "Enable", and you should be all set! 

## I installed the extension. Why isn't it working?

Currently, this extension only works with Review Board 1.7.15 and higher. Make sure your Review Board instance is up to date.
