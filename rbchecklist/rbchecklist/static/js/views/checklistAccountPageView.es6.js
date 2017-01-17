/**
 * The view for displaying a checklist template.
 */
Checklist.TemplateView = Backbone.View.extend({
    className: 'rbchecklist-template',

    events: {
        'click .rbchecklist-template-action-remove': '_removeTemplate',
        'click .rbchecklist-template-action-edit': '_editTemplate',
    },

    template: _.template(dedent`
        <ul class="rbchecklist-template-items"></ul>
        <div class="rbchecklist-template-actions">
         <input class="rbchecklist-template-action-edit btn" type="button"
                value="Edit">
         <input class="rbchecklist-template-action-remove btn danger"
                type="button" value="Remove">
        </div>
    `),

    /**
     * Iritialize the view.
     */
    initialize() {
        this.render();

        this.listenTo(this.model, 'destroy', this.remove);
        this.listenTo(this.model, 'update show', this._show);
    },

    /**
     * Render the view.
     *
     * Returns:
     *     Checklist.TemplateView:
     *     This object, for chaining.
     */
    render() {
        this.$el.html(this.template());

        const $items = this.$el.children('.rbchecklist-template-items');

        $('<li class="rbchecklist-template-title" />')
            .text(this.model.get('title'))
            .appendTo($items);

        const items = this.model.get('items');
        items.forEach(item =>
            $('<li class="rbchecklist-template-item" />')
                .text(item)
                .appendTo($items)
        );

        return this;
    },

    /**
     * Edit the template.
     *
     * Hide this view and show an edit view of the same model.
     */
    _editTemplate() {
        const editView = new Checklist.TemplateEditView({
            collection: this.collection,
            model: this.model,
        });

        this.$el
            .hide()
            .before(editView.$el);
    },

    /**
     * Remove the template.
     */
    _removeTemplate() {
        var collection = this.model.collection;

        this.model.destroy({
            wait: true,
            success: () => collection.remove(this.model),
        });
    },

    /**
     * Show the template.
     */
    _show() {
        this.render();
        this.$el.show();
    },
});


/**
 * The view for editing a checklist template.
 */
Checklist.TemplateEditView = Backbone.View.extend({
    className: 'rbchecklist-template-edit',

    events: {
        'click #rbchecklist-template-action-save': '_saveTemplate',
        'click input[name=cancel]': '_cancel',
        'keyup input[name=item]': '_editItem',
        'keydown input[name=item]': '_nextItem',
    },

    /**
     * Template for a checklist item input field.
     */
    _itemInputField: dedent`
        <input type="text" name="item"',
               class="rbchecklist-template-edit-item">
    `,

    template: _.template(dedent`
        <div class="rbchecklist-template-list">
         <input type="text" name="title" placeholder="Title"
               class="rbchecklist-template-edit-title">
         <input type="text" name="item"
               class="rbchecklist-template-edit-item">
        </div>
        <div class="rbchecklist-template-actions">
         <input type="submit" value="Save"
                id="rbchecklist-template-action-save">
         <input type="button" value="Cancel" name="cancel">
        </div>
    `),

    /**
     * Initialize the view.
     *
     * Args:
     *     options (object):
     *         Options for the view.
     *
     * Option Args:
     *     model (Checklist.Template):
     *         The model for the view.
     *
     *     collection (Checklist.TemplateCollection):
     *         The collection containing the model.
     */
    initialize(options) {
        this.model = options.model || new Checklist.Template();
        this.collection = options.collection || this.model.collection;

        this.render();
    },

    /**
     * Render the view.
     *
     * Returns:
     *     Checklist.TemplateEditView:
     *     This object, for chaining.
     */
    render() {
        this.$el.html(this.template(this.model.toJSON()));

        this._$inputFields = this.$('.rbchecklist-template-list');

        this._$inputFields.children('input[name=title]')
            .val(this.model.get('title'));

        const $firstInput = this._$inputFields.children('input[name=item]').first();

        this.model.get('items').forEach(
            item => $firstInput.before($(this._itemInputField).val(item)));

        return this;
    },

    /**
     * Save the template.
     *
     * Update or add model to collection when put or post is successful.
     *
     * Args:
     *     ev (Event):
     *         The event that triggered the action.
     */
    _saveTemplate(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        const title = this._$inputFields.children('input[name=title]').val();
        const $items = this._$inputFields.children('input[name=item]');

        // Map item input fields to a normal array, and filter empty values.
        const items = $items
            .map((i, el) => $(el).val().trim())
            .get()
            .filter(value => value !== '');

        this.listenToOnce(this.model, 'sync', () => {
            this.collection.push(this.model);
            this.remove();
        });

        this.model.save({
            title: title,
            items: items
        });
    },

    /**
     * Cancel the template edit.
     *
     * Remove this view and trigger change on model to unhide original view.
     */
    _cancel() {
        if (!this.model.isNew()) {
            this.model.trigger('show');
        }

        this.remove();
    },

    /**
     * Add a new input field if last input field is not empty.
     */
    _editItem() {
        const $lastItemInput = this._$inputFields.children('input[name=item]').last();

        if ($lastItemInput.val().trim() !== '') {
            $lastItemInput.after($(this._itemInputField));
        }
    },

    /**
     * Focus and select next input field when enter is pressed.
     *
     * Args:
     *     ev (Event):
     *         The event which triggered the action.
     */
    _nextItem(ev) {
        if (ev.keyCode === $.ui.keyCode.ENTER || ev.keyCode === 13) {
            ev.preventDefault();
            ev.stopPropagation();

            const $nextItemInput = $(ev.target).next();

            if ($nextItemInput.is('input[name=item]')) {
                $nextItemInput.select();
            }
        }
    },
});


/**
 * The view that is instantiated by the account page.
 */
Checklist.AccountPageView = Backbone.View.extend({
    template: _.template(dedent`
        <div class="rbchecklist-accountpage">
         <div class="rbchecklist-actions">
          <input type="button" value="New template"
                 id="rbchecklist-template-add-new">
         </div>
         <div class="rbchecklist-templates"></div>
        </div>
    `),

    events: {
        'click #rbchecklist-template-add-new': '_addTemplate',
    },

    /**
     * Initialize the view.
     */
    initialize: function() {
        this.render();

        this.collection = new Checklist.TemplateCollection();
        this.listenTo(this.collection, 'add', template => {
            const templateView = new Checklist.TemplateView({
                model: template,
            });

            templateView.$el.prependTo(this.$templatesView);
        });
        this.collection.fetch();
    },

    /**
     * Render the view.
     *
     * Returns:
     *     Checklist.AccountPageView:
     *     This object, for chaining.
     */
    render: function() {
        this.$el.html(this.template());
        this.$templatesView = this.$el.find('.rbchecklist-templates');

        return this;
    },

    /**
     * Add a new template.
     *
     * Show and focus on the view that creates a new checklist template.
    */
    _addTemplate: function() {
        const newTemplateView = new Checklist.TemplateEditView({
            collection: this.collection,
        });
        this.$templatesView.before(newTemplateView.$el);
        newTemplateView.$el.find('input[name=title]').focus();
    },
});
