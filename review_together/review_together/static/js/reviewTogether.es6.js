window.ReviewTogetherJS = {};


/**
 * Extends Review Board with TogetherJS capabilities.
 */
ReviewTogetherJS.Extension = RB.Extension.extend({
    /**
     * Initialize the extension.
     */
    initialize() {
        RB.Extension.prototype.initialize.call(this);

        const settings = this.get('settings');

        if (settings.hub_url) {
            TogetherJSConfig_hubBase = settings.hub_url.trim();
        }

        const together = $('#launch-together');

        if (together) {
            together.click(function() {
                TogetherJS(this);
            });
        }

        TogetherJS.on('close',
                      () => $('.togetherjs-peer-scroll-position').remove());

        TogetherJS.on('ready', () => {
            TogetherJS.require('session').hub.on('bye', peer_transmission => {
                const peer = peer_transmission.peer;

                if (peer) {
                    const id = peer.id.split('.')[0];
                    $(`.togetherjs-peer-scroll-position[peerID="${id}"]`).remove();
                }
            });
        });

        document.addEventListener('scroll', () => {
            if (!TogetherJS.running) {
                return;
            }

            const scrollPosition = $(document).scrollTop();
            const peerObject = TogetherJS.require('peers').Self;

            TogetherJS.send({
                type: 'scroll',
                position: scrollPosition,
                color: peerObject.color,
                identityId: peerObject.identityId,
            });
        });
    }
});


/**
 * Event handler for when a peer sends you a scroll event.
 */
TogetherJS.hub.on('scroll', peer_transmission => {
    const peerPosition = parseInt(peer_transmission.position, 10);
    const peerColor = peer_transmission.color;
    const id = peer_transmission.identityId;
    let $scroll = $('.togetherjs-peer-scroll-position[peerID="${id}"]');

    // Create the scroll position if it has not already been created.
    if (!$scroll.length) {
        $scroll = $('<div>')
            .addClass('togetherjs-peer-scroll-position')
            .attr('peerID', id)
            .appendTo(document.body);
    }

    // Set the position and color of the scroll position bar.
    $scroll.css({
        'background-color': peerColor,
        top: peerPosition,
    });
});
