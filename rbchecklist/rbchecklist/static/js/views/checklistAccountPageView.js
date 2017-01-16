(function() {


/*
 * The view for displaying a checklist template.
 */
ChecklistTemplateView = Backbone.View.extend({
    className: 'rbchecklist-template',

    events: {
        'click .rbchecklist-template-action-remove': '_removeTemplate',
        'click .rbchecklist-template-action-edit': '_editTemplate'
    },

    template: _.template([
        '<ul class="rbchecklist-template-items" />',
        '<div class="rbchecklist-template-actions">',
        ' <input class="rbchecklist-template-action-edit btn" type="button"',
        '        value="Edit">',
        ' <input class="rbchecklist-template-action-remove btn danger"',
        '        type="button" value="Remove" />',
        '</div>'
    ].join('')),

    initialize: function(options) {
        this.render();

        /* Remove the view when the model is destroyed. */
        this.listenTo(this.model, 'destroy', this.remove);

        /* Re-render the view when shown or the model is updated. */
        this.listenTo(this.model, 'update show', this._show);
    },

    /* Render .template and individual checklist items. */
    render: function() {
        var items = this.model.get('items'),
            $items;

        this.$el.html(this.template());

        $items = this.$el.children('.rbchecklist-template-items');
        $('<li class="rbchecklist-template-title" />')
            .text(this.model.get('title'))
            .appendTo($items);

        _.each(items, function(item) {
            $('<li class="rbchecklist-template-item" />')
                .text(item)
                .appendTo($items);
        });

        return this;
    },

    /*
     * Edit button handler.
     *
     * Hide this view and show an edit view of the same model.
     */
    _editTemplate: function(event) {
        var editView = new ChecklistTemplateEditView({
            collection: this.collection,
            model: this.model
        });

        this.$el
            .hide()
            .before(editView.$el);
    },

    /*
     * Remove button handler.
     *
     * Remove model from the collection after delete is successful.
     */
    _removeTemplate: function(event) {
        var collection = this.model.collection;

        this.model.destroy({
            wait: true,
            success: _.bind(function(model, response) {
                collection.remove(this.model);
            }, this)
        });
    },

    /*
     * Model on show handler.
     *
     * Re-render and show the view.
     */
    _show: function(event, a) {
        this.render();
        this.$el.show();
    }
});


/*
 * The view for editing a checklist template.
 */
ChecklistTemplateEditView = Backbone.View.extend({
    className: 'rbchecklist-template-edit',

    events: {
        'click #rbchecklist-template-action-save': '_saveTemplate',
        'click input[name=cancel]': '_cancel',
        'keyup input[name=item]': '_editItem',
        'keydown input[name=item]': '_nextItem'
    },

    /* Template for a checklist item input field. */
    _itemInputField: [
        '<input type="text" name="item"',
        '       class="rbchecklist-template-edit-item" />'
    ].join(''),

    template: _.template([
        '<div class="rbchecklist-template-list">',
        ' <input type="text" name="title" placeholder="Title"',
        '       class="rbchecklist-template-edit-title" />',
        ' <input type="text" name="item"',
        '       class="rbchecklist-template-edit-item" />',
        '</div>',
        '<div class="rbchecklist-template-actions">',
        ' <input type="submit" value="Save"',
        '        id="rbchecklist-template-action-save" />',
        ' <input type="button" value="Cancel" name="cancel" />',
        '</div>'
    ].join('')),

    initialize: function(options) {
        this.model = options.model || new ChecklistTemplate();
        this.collection = options.collection || this.model.collection;

        this.render();
    },

    /* Render template and individual checklist items. */
    render: function() {
        var $firstInput;

        this.$el.html(this.template(this.model.toJSON()));

        this._$inputFields = this.$el.children('.rbchecklist-template-list');

        this._$inputFields.children('input[name=title]')
            .val(this.model.get('title'));

        $firstInput = this._$inputFields.children('input[name=item]').first();

        _.each(this.model.get('items'), _.bind(function(item) {
            $firstInput.before($(this._itemInputField).val(item));
        }, this));

        return this;
    },

    /*
     * Save button handler.
     *
     * Update or add model to collection when put or post is successful.
     */
    _saveTemplate: function(event) {
        var template,
            items,
            title = this._$inputFields.children('input[name=title]').val(),
            $items = this._$inputFields.children('input[name=item]');

        event.preventDefault();

        // Map item input fields to a normal array, and filter empty values.
        items = $items.map(function() {
            return $(this).val().trim();
        }).toArray();
        items = _.filter(items, function(val) {
            return val !== '';
        });

        this.listenToOnce(this.model, 'sync', this._saved);

        this.model.save({
            title: title,
            items: items
        });

        return false;
    },

    /*
     * Model on sync handler.
     *
     * Add model to or update model in collection.
     */
    _saved: function() {
        this.collection.push(this.model);
        this.remove();
    },

    /*
     * Cancel button handler.
     *
     * Remove this view and trigger change on model to unhide original view.
     */
    _cancel: function(event) {
        if (!this.model.isNew()) {
            this.model.trigger('show');
        }
        this.remove();
    },

    /* Add new input field if last input field is not empty. */
    _editItem: function(event) {
        $lastItemInput = this._$inputFields.children('input[name=item]').last();
        if ($lastItemInput.val().trim() !== '') {
            $lastItemInput.after($(this._itemInputField));
        }
    },

    /* Focus and select next input field when enter is pressed. */
    _nextItem: function(event) {
        if (event.keyCode === $.ui.keyCode.ENTER || event.keyCode === 13) {
            event.preventDefault();
            $nextItemInput = $(event.target).next();
            if ($nextItemInput.is('input[name=item]')) {
                $nextItemInput.select();
            }
            return false;
        }
        return true;
    }
});


/*
 * The view that is instantiated by the account page.
 */
RB.ChecklistAccountPageView = Backbone.View.extend({
    template: _.template([
        '<div class="rbchecklist-accountpage">',
        ' <div class="rbchecklist-actions">',
        '  <input type="button" value="New template"',
        '         id="rbchecklist-template-add-new" />',
        ' </div>',
        ' <div class="rbchecklist-templates" />',
        '</div>'
    ].join('')),

    events: {
        'click #rbchecklist-template-add-new': '_showAddNewTemplateView'
    },

    initialize: function() {
        this.collection = new ChecklistTemplateCollection();
        this.listenTo(this.collection, 'add', this._addTemplate);
        this.collection.fetch();

        this.render();
    },

    /* Prepend to $templatesView when a template is added to the collection. */
    _addTemplate: function(template) {
        var templateView = new ChecklistTemplateView({
            model: template
        });
        templateView.$el.prependTo(this.$templatesView);
    },

    /* Render the view and keep track of the templates view. */
    render: function() {
        this.$el.html(this.template());
        this.$templatesView = this.$el.find('.rbchecklist-templates');
        return this;
    },

    /*
     * New template button on click handler.
     *
     * Show and focus on the view that creates a new checklist template.
    */
    _showAddNewTemplateView: function() {
        var newTemplateView = new ChecklistTemplateEditView({
            collection: this.collection
        });
        this.$templatesView.before(newTemplateView.$el);
        newTemplateView.$el.find('input[name=title]').focus();
    }
});


})();
