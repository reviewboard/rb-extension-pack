RBSeverity = {};


/*
 * Extends the comment dialog to provide buttons for severity.
 *
 * The Save button will be removed, and in its place will be a set of
 * buttons for choosing the severity level for the comment. The buttons
 * each work as save buttons.
 */
RBSeverity.CommentDialogHookView = Backbone.View.extend({
    events: {
        'click .buttons .save-major': '_onSaveMajorClicked',
        'click .buttons .save-minor': '_onSaveMinorClicked',
        'click .buttons .save-info': '_onSaveInfoClicked'
    },

    buttonsTemplate: _.template([
        '<span class="severity-actions">',
        '  <input type="button" class="save-major" value="Major" ',
        '         disabled="true" />',
        '  <input type="button" class="save-minor" value="Minor" ',
        '         disabled="true" />',
        '  <input type="button" class="save-info" value="Info" ',
        '         disabled="true" />',
        '</span>'
    ].join('')),

    /*
     * Initializes the view.
     */
    initialize: function(options) {
        this.commentDialog = options.commentDialog;
        this.commentEditor = options.commentEditor;
    },

    /*
     * Renders the additions to the comment dialog.
     *
     * This will remove the Save button and set up the new buttons.
     */
    render: function() {
        var $severityButtons = $(this.buttonsTemplate());

        this.commentDialog.$saveButton.remove();
        this.commentDialog.$buttons.prepend($severityButtons);

        $severityButtons.find('input')
            .bindVisibility(this.commentEditor, 'canEdit')
            .bindProperty('disabled', this.commentEditor, 'canSave', {
                elementToModel: false,
                inverse: true
            });

        /* Set a default severity, in case the user hits Control-Enter. */
        this.commentEditor.setExtraData('severity', 'info');
    },

    /*
     * Handler for when the "Major" button is clicked.
     *
     * Saves the comment with a "Major" severity.
     */
    _onSaveMajorClicked: function() {
        this._saveCommon('major');
    },

    /*
     * Handler for when the "Minor" button is clicked.
     *
     * Saves the comment with a "Minor" severity.
     */
    _onSaveMinorClicked: function() {
        this._saveCommon('minor');
    },

    /*
     * Handler for when the "Info" button is clicked.
     *
     * Saves the comment with an "Info" severity.
     */
    _onSaveInfoClicked: function() {
        this._saveCommon('info');
    },

    /*
     * Common function for saving with a severity.
     *
     * This will set the severity for the comment and then save it.
     */
    _saveCommon: function(severity) {
        if (this.commentEditor.get('canSave')) {
            this.commentEditor.setExtraData('severity', severity);
            this.commentDialog.save();
        }
    }
});


/*
 * Extends the review dialog to allow setting severities on unpublished
 * comments.
 *
 * A field will be provided that contains a list of severities to choose
 * from.
 *
 * If the comment does not have any severity set yet (meaning it's a pending
 * comment from before the extension was activated), a blank entry will be
 * added. If the severity is then set, the blank entry will go away the next
 * time it's loaded.
 */
RBSeverity.ReviewDialogCommentHookView = Backbone.View.extend({
    events: {
        'change select': '_onSeverityChanged'
    },

    template: _.template([
        '<label for="<%- id %>">Severity:</label> ',
        '<select id="<%- id %>">',
        ' <option value="major">Major</option>',
        ' <option value="minor">Minor</option>',
        ' <option value="info">Info</option>',
        '</select>'
    ].join('')),

    /*
     * Renders the editor for a comment's severity.
     */
    render: function() {
        var severity = this.model.get('extraData').severity;

        this.$el.html(this.template({
            id: 'severity_' + this.model.id
        }));

        this._$select = this.$('select');

        if (severity) {
            this._$select.val(severity);
        } else {
            this._$select.prepend($('<option selected/>'));
        }

        return this;
    },

    /*
     * Handler for when the severity is changed by the user.
     *
     * Updates the severity on the comment to match.
     */
    _onSeverityChanged: function() {
        this.model.get('extraData').severity = this._$select.val();
    }
});


/*
 * Extends Review Board with comment severity support.
 *
 * This plugs into the comment dialog and review dialog to add the ability
 * to set severities for comments.
 */
RBSeverity.Extension = RB.Extension.extend({
    initialize: function() {
        _super(this).initialize.call(this);

        new RB.CommentDialogHook({
            extension: this,
            viewType: RBSeverity.CommentDialogHookView
        });

        new RB.ReviewDialogCommentHook({
            extension: this,
            viewType: RBSeverity.ReviewDialogCommentHookView
        });
    }
});
