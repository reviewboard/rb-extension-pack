var ReviewTogetherJS = {};

/*
 * Extends Review Board with TogetherJS capabilities.
 */
ReviewTogetherJS.Extension = RB.Extension.extend({
    initialize: function () {
        _super(this).initialize.call(this);

        var settings = this.get('settings');

        if (settings.hub_url.trim()) {
            TogetherJSConfig_hubBase = settings.hub_url;
        }

        var together = $("#launch-together");
        if (together) {
            together.click(function () {
                TogetherJS(this);
            });
        }
    }
});
