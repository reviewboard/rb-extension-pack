ReviewTogetherJS = {};

(function() {
    /*
     * Extends Review Board with TogetherJS capabilities.
     */
    ReviewTogetherJS.Extension = RB.Extension.extend({
        initialize: function () {
            var settings,
                together;

            _super(this).initialize.call(this);

            settings = this.get('settings');

            if (settings.hub_url) {
                TogetherJSConfig_hubBase = settings.hub_url.trim();
            }

            together = $('#launch-together');
            if (together) {
                together.click(function () {
                    TogetherJS(this);
                });
            }

            TogetherJS.on('close', function() {
                $('.togetherjs-peer-scroll-position').remove();
            });

            TogetherJS.on('ready', function() {
                TogetherJS.require('session').hub.on('bye', function(peer_transmission) {
                    var peer = peer_transmission.peer,
                        peer_identityId;

                    if (peer) {
                        peer_identityId = peer.id.split('.')[0];
                        $('.togetherjs-peer-scroll-position[peerID="' +
                          peer_identityId + '"]').remove();
                    }
                });
            });

            document.addEventListener('scroll', documentScroll);
        }
    });

    /**
     * This callback function sends data to the peer when the scroll
     * position is updated.
     */
    function documentScroll() {
        var scroll_position,
            peer_object;

        if (!TogetherJS.running) {
            return;
        }

        scroll_position = $(document).scrollTop();
        peer_object = TogetherJS.require('peers').Self;

        TogetherJS.send({
            type: 'scroll',
            position: scroll_position,
            color: peer_object.color,
            identityId: peer_object.identityId,
        });
    }

    /**
     * Event handler for when a peer sends you a scroll event.
     */
    TogetherJS.hub.on('scroll', function (peer_transmission) {
        var peer_position = parseInt(peer_transmission.position, 10),
            peer_color = peer_transmission.color,
            peer_identityId = peer_transmission.identityId,
            scroll_position_bar =
                $('.togetherjs-peer-scroll-position[peerID="' +
                  peer_identityId + '"]');

        // Create the scroll position if it has not already been created.
        if (!scroll_position_bar.length) {
            scroll_position_bar = $('<div/>')
                                    .addClass('togetherjs-peer-scroll-position')
                                    .attr('peerID', peer_identityId)
                                    .appendTo(document.body);
        }

        // The colour may have been updated since construction.
        scroll_position_bar.css('background-color', peer_color);

        // Set the position of the peer scroll position div.
        scroll_position_bar.css({top: peer_position});
    });
})();
