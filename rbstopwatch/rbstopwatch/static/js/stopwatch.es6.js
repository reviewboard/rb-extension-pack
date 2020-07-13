window.RBStopwatch = {};


/**
 * Format a number of seconds into a string showing the amount of elapsed time.
 *
 * Args:
 *     totalSeconds (number):
 *         The elapsed number of seconds.
 *
 * Returns:
 *     string:
 *     The formatted string.
 */
RBStopwatch.formatTimeString = function(totalSeconds) {
    const hours = Math.floor(totalSeconds / 3600).toFixed(0);
    const minutes = Math.floor((totalSeconds % 3600) / 60).toFixed(0);
    const seconds = Math.floor(totalSeconds % 60).toFixed(0);

    let display = (hours < 10) ? '0' + hours : hours;
    display += ':';
    display += (minutes < 10) ? '0' + minutes : minutes;
    display += ':';
    display += (seconds < 10) ? '0' + seconds : seconds;

    return display;
};


/**
 * The stopwatch model.
 *
 * This includes the timer machinery and serialization into the pending review.
 */
RBStopwatch.Stopwatch = Backbone.Model.extend({
    defaults: {
        pendingReview: null,
        timerOn: false,
        totalSec: 0,
    },

    /**
     * Initialize the model.
     *
     * Args:
     *     attrs (object):
     *         Attribute values for the model.
     */
    initialize(attrs) {
        _.bindAll(this, 'toggle', '_onReviewDone', '_onTick');

        Backbone.Model.prototype.initialize.apply(this, arguments);

        this._startTime = null;
        this._timerHandle = null;

        const pendingReview = attrs.pendingReview;
        console.assert(pendingReview);

        const extraData = pendingReview.get('extraData') || {};
        const currentTime = parseInt(extraData['rbstopwatch.reviewTime'], 10) || 0;

        this.set('totalSec', currentTime);
        this._currentTime = currentTime;

        this.listenTo(pendingReview, 'destroy', this._onReviewDone);
        this.listenTo(pendingReview, 'publishing', this._onReviewDone);
    },

    /**
     * Toggle the stopwatch on or off.
     */
    toggle() {
        if (this._timerHandle) {
            this._stop();
        } else {
            this._start();
        }
    },

    /**
     * Start the stopwatch.
     */
    _start() {
        console.assert(this._timerHandle === null);

        this._startTime = Date.now();
        this._timerHandle = window.setInterval(this._onTick, 1000);

        this.set('timerOn', true);
    },

    /**
     * Stop the stopwatch.
     *
     * Args:
     *     options (object, optional):
     *         Options for the operation.
     *
     * Option Args:
     *     skipSave (boolean):
     *         Whether to skip saving the stopwatch value.
     */
    _stop(options={}) {
        console.assert(this._timerHandle !== null);
        console.assert(this._startTime !== null);

        window.clearInterval(this._timerHandle);
        this._timerHandle = null;

        const addedTime = Math.floor((Date.now() - this._startTime) / 1000);
        this._currentTime += addedTime;
        this.set({
            totalSec: this._currentTime,
            timerOn: false
        });

        const pendingReview = this.get('pendingReview');
        const extraData = pendingReview.get('extraData');
        extraData['rbstopwatch.reviewTime'] = this._currentTime;
        pendingReview.set('extraData', extraData);

        if (options.skipSave !== true) {
            pendingReview.save();
            RB.DraftReviewBannerView.instance.show();
        }
    },

    /**
     * Handler for events which signify that the review is "done" (notably
     * 'destroy' and 'publishing').
     *
     * If the stopwatch is currently running, stop it and set the results in
     * the model without saving it to the server.
     */
    _onReviewDone() {
        if (this.get('timerOn')) {
            this._stop({skipSave: true});
        }
    },

    /**
     * Handle a tick. This updates the 'totalSec' attribute;
     */
    _onTick() {
        console.assert(this._startTime !== null);

        const addedTime = Math.floor((Date.now() - this._startTime) / 1000);
        this.set('totalSec', this._currentTime + addedTime);
    },
}, {
    instance: null,

    /**
     * Create the stopwatch model singleton.
     *
     * Args:
     *     attrs (object):
     *         Model attribute values.
     *
     * Returns:
     *     RBStopwatch.Stopwatch:
     *     The stopwatch model instance.
     */
    create(attrs) {
        if (!this.instance) {
            this.instance = new RBStopwatch.Stopwatch(attrs);
        }

        return this.instance;
    },
});


/**
 * The stopwatch view.
 */
RBStopwatch.StopwatchView = Backbone.View.extend({
    id: 'rbstopwatch-stopwatch',

    template: _.template(dedent`
        <div class="<%- stopwatchClass %>">
         &#x1F551;<%- display %>
        </div>
    `),

    events: {
        'click': 'toggle',
    },

    /**
     * Initialize the view
     */
    initialize() {
        this.listenTo(this.model, 'change', this.render);

        window.addEventListener('beforeunload',
                                _.bind(this.beforeUnload, this));
    },

    /**
     * Render the view
     *
     * Returns:
     *     RBStopwatch.StopwatchView:
     *     This object, for chaining.
     */
    render() {
        var totalSec = this.model.get('totalSec'),
            timerOn = this.model.get('timerOn'),
            display = RBStopwatch.formatTimeString(totalSec);

        this.$el.html(this.template({
            display: display,
            stopwatchClass: timerOn ? 'rbstopwatch-on' : 'rbstopwatch-off'
        }));

        return this;
    },

    /**
     * Toggle the stopwatch on or off.
     */
    toggle() {
        this.model.toggle();
    },

    /**
     * Handler for the window's beforeunload event.
     *
     * This confirms that users want to navigate away while the stopwatch
     * is running.
     *
     * Args:
     *     ev (Event):
     *         The beforeunload event.
     */
    beforeUnload(ev) {
        if (this.model.get('timerOn')) {
            const message = ('The review stopwatch is still running. If you ' +
                             'leave without stopping it, the timer info for ' +
                             'this page will be lost.');

            (ev || window.event).returnValue = message;
            return message;
        }

        return null;
    },
});


RBStopwatch.ReviewDialogHookView = Backbone.View.extend({
    template: _.template(dedent`
        <%- prefixText %>
        <span class="<%- className %>"><%- timeText %></div>
    `),

    /**
     * Initialize the view.
     */
    initialize() {
        const stopwatch = RBStopwatch.Stopwatch.instance;

        if (stopwatch) {
            this.listenTo(stopwatch, 'change', this.render);
        }
    },

    /**
     * Render the view.
     *
     * Returns:
     *     RBStopwatch.ReviewDialogHookView:
     *     This object, for chaining.
     */
    render() {
        const stopwatch = RBStopwatch.Stopwatch.instance;
        let currentTime;
        let timerOn = false;

        if (stopwatch) {
            timerOn = stopwatch.get('timerOn');
            currentTime = stopwatch.get('totalSec');
        } else {
            const extraData = this.model.get('extraData') || {};
            currentTime = parseInt(extraData['rbstopwatch.reviewTime'], 10) || 0;
        }

        if (currentTime) {
            this.$el.html(this.template({
                className: timerOn ? 'rbstopwatch-on' : 'rbstopwatch-off',
                prefixText: gettext('Total time spent on this review:'),
                timeText: RBStopwatch.formatTimeString(currentTime)
            }));
        } else {
            this.$el.empty();
        }

        return this;
    },
});


/**
 * Extends Review Board with a stopwatch to track total review time.
 */
RBStopwatch.Extension = RB.Extension.extend({
    /**
     * Initialize the extension.
     */
    initialize() {
        RB.Extension.prototype.initialize.call(this);

        this.reviewDialogHook = new RB.ReviewDialogHook({
            extension: this,
            viewType: RBStopwatch.ReviewDialogHookView,
        });

        RB.PageManager.ready(page => {
            const pendingReview = page.pendingReview;

            pendingReview.ready({
                ready: () => {
                    this.stopwatchView = new RBStopwatch.StopwatchView({
                        model: RBStopwatch.Stopwatch.create({
                            pendingReview: pendingReview,
                        }),
                    });

                    this.stopwatchView.render();
                    $('body').append(this.stopwatchView.$el);
                },
            });
        });
    },
});
