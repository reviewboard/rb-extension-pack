var ReviewTogetherJS = {};

/*
 * Extends Review Board with TogetherJS capabilities.
 */
ReviewTogetherJS.Extension = RB.Extension.extend({
    initialize: function () {
        _super(this).initialize.call(this);

        var settings = this.get('settings');

        TogetherJSConfig_hubBase = settings.hub_url;

        var together = $("#launch-together");

        if (together) {
            together.click(function () {
                TogetherJS(this);
            });
        }

        document.addEventListener("scroll", documentScroll);
    }
});

/*
 * This callback function sends data to the peer when scroll position is updated.
 */
function documentScroll() {
    var scroll_position = $(document).scrollTop();
    var peer_object = TogetherJS.require("peers").Self;
    // Do not send scroll position if the user is scrolling up higher than the top
    // of the page.
    if (scroll_position > 0) {
        TogetherJS.send({
            type: "scroll",
            position: scroll_position,
            color: peer_object.color,
            identityId: peer_object.identityId,
        });
    }
}


TogetherJSConfig_on_close = function () {
    // Remove scroll event when the extension is closed.
    document.removeEventListener("scroll", documentScroll);
};
/*
 * Event handler when a peer sends you a scroll event.
 */
TogetherJS.hub.on("scroll", function (peer_transmission) {
    var peer_position = parseInt(peer_transmission.position, 10);
        peer_color = peer_transmission.color,
        peer_identityId = peer_transmission.identityId,
        scroll_position_bar =
            $("#" + peer_identityId + ".togetherjs-peer-scroll-position");

    // Create the scroll position if it has not already been created.
    if (!scroll_position_bar.length) {
        $('<div/>')
          .attr("id", peer_identityId)
          .addClass("togetherjs-peer-scroll-position")
          .css("background-color", peer_color)
          .appendTo(document.body);

        scroll_position_bar =
            $("#" + peer_identityId + ".togetherjs-peer-scroll-position");
    }

    var scroll_position_bar_height = scroll_position_bar.height();

    // Set the position of the peer scroll position div.
    scroll_position_bar.css({top: peer_position - scroll_position_bar_height});

    // Hide the scroll position if the peer is close to the top of the page.
    var hide_bar = peer_position >= scroll_position_bar_height*2;
    scroll_position_bar.toggle(hide_bar);
});
