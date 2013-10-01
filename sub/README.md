reviewboard_together
====================

Review Board is a web-based code review tool that takes the pain out of code review.

[Mozilla Labs' TogetherJS](http://togetherjs.com/) (formerly TowTruck) makes it easy to let the viewers of a web page
chat with one another - either via text, or over WebRTC with their microphones.

reviewboard_together is an extension for Review Board that lets users chat via TogetherJS.

## I installed the extension. Why isn't it working?

Currently, this extension only works with a development install of Review Board. The HeaderActionHooks that the extension depends on will hopefully be backported to 1.7 soon, and then this extension will then be compatible with the release version of Review Board.
