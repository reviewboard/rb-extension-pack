RBCommentType = {};


/*
 * Set a default empty list for the configured types. This will get overridden
 * in the rbcommenttypes-types.html template hook.
 */
RBCommentType.configuredTypes = [];


/*
 * A mixin for common functionality between views.
 */
var CommentTypeUtilMixin = {
    /*
     * Pre-select the current type.
     */
    selectExistingType: function(type, $select) {
        var allowEmpty = (RBCommentType.configuredTypes.length &&
                          RBCommentType.configuredTypes[0].length === 0);

        if (type) {
            $select.val(type);
        } else {
            if (!allowEmpty) {
                /*
                 * If a comment existed before users were forced to choose a
                 * type, prepend an empty option even if types aren't required.
                 * This way we don't auto-select something for users if they
                 * didn't choose it.
                 */
                $select.prepend('<option selected/>');
            }
        }
    }
};


/*
 * Extends the comment dialog to provide a drop-down for the comment type.
 */
RBCommentType.CommentDialogHookView = Backbone.View.extend(_.extend({
    events: {
        'change select': '_onTypeChanged'
    },

    template: _.template([
        '<label for="<%- id %>">Type: </label>',
        '<select id="<%- id %>">',
        ' <% _.each(types, function(type) { %>',
        '  <option value="<%- type %>"><%- type %></option>',
        ' <% }); %>',
        '</select>'
    ].join('')),

    /*
     * Initialize the view.
     */
    initialize: function(options) {
        this.commentDialog = options.commentDialog;
        this.commentEditor = options.commentEditor;
    },

    /*
     * Render the editor for a comment's type.
     */
    render: function() {
        var $li = $('<li class="comment-type" />')
            .html(this.template({
                id: 'comment_type_' + this.commentEditor.cid,
                types: RBCommentType.configuredTypes
            }));

        this.$('.comment-type').remove();
        this.$('.comment-dlg-options').append($li);

        this._$select = $li.find('select')
            .bindVisibility(this.commentEditor, 'canEdit');

        this.selectExistingType(this.commentEditor.getExtraData('commentType'),
                                this._$select);

        return this;
    },

    /*
     * Handler for when the type is changed by the user.
     *
     * Updates the type on the comment model to match.
     */
    _onTypeChanged: function() {
        this.commentEditor.setExtraData('commentType', this._$select.val());
    }
}, CommentTypeUtilMixin));


/*
 * Extends the review dialog to allow setting comment types on unpublished
 * comments.
 */
RBCommentType.ReviewDialogCommentHookView = Backbone.View.extend(_.extend({
    events: {
        'change select': '_onTypeChanged'
    },

    template: _.template([
        '<label for="<%- id %>">Type: </label>',
        '<select id="<%- id %>">',
        ' <% _.each(types, function(type) { %>',
        '  <option value="<%- type %>"><%- type %></option>',
        ' <% }); %>',
        '</select>'
    ].join('')),

    /*
     * Render the editor for a comment's type.
     */
    render: function() {
        this.$el.html(this.template({
            id: 'comment_type_' + this.model.id,
            types: RBCommentType.configuredTypes
        }));

        this._$select = this.$('select');
        this.selectExistingType(this.model.get('extraData').commentType,
                                this._$select);

        return this;
    },

    /*
     * Handler for when the type is changed by the user.
     *
     * Updates the type on the comment model to match.
     */
    _onTypeChanged: function() {
        var extraData = this.model.get('extraData');

        extraData.commentType = this._$select.val();
        this.model.set('extraData', extraData);
    }
}, CommentTypeUtilMixin));


/*
 * Extends Review Board with comment type categorization.
 *
 * This plugs into the comment dialog and review dialog to add the ability to
 * set types for comments.
 */
RBCommentType.Extension = RB.Extension.extend({
    initialize: function() {
        _super(this).initialize.call(this);

        new RB.CommentDialogHook({
            extension: this,
            viewType: RBCommentType.CommentDialogHookView
        });

        new RB.ReviewDialogCommentHook({
            extension: this,
            viewType: RBCommentType.ReviewDialogCommentHookView
        });
    }
});
