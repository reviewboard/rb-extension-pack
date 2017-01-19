{


/**
 * The view for each item on the checklist.
 */
Checklist.ChecklistItemView = Backbone.View.extend({
    tagName: 'li',
    className: 'checklist-item',

    events: {
        'click input[name="checklist-checkbox"]': '_onToggleClicked',
        'click .checklist-item-description': '_startEdit',
        'click .checklist-item-edit': '_startEdit',
        'click .checklist-item-edit-accept': '_confirmEdit',
        'click .checklist-item-edit-cancel': '_cancelEdit',
        'click .checklist-item-delete': '_onRemoveClicked',
        'keydown .checklist-item-description': '_onEditKeyDown',
    },

    /**
     * The template for items in their default state.
     */
    template: _.template(dedent`
        <div class="checklist-checkbox-container">
         <input type="checkbox" name="checklist-checkbox"
                <% if (checked) { %> checked <% } %> >
        </div>
        <div class="checklist-description-container">
         <div class="checklist-item-actions">
          <span class="fa fa-pencil checklist-item-edit"></span>
          <span class="fa fa-trash-o checklist-item-delete"></span>
          <span class="fa fa-check checklist-item-edit-accept"></span>
          <span class="fa fa-close checklist-item-edit-cancel"></span>
         </div>
         <span class="checklist-item-description"><%- description %></span>
        </div>
    `),

    /**
     * Initialize the view.
     */
    initialize() {
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destroy', this.remove);

        this.render();
    },

    /**
     * Render the view.
     *
     * Returns:
     *     Checklist.ChecklistItemView:
     *     This object, for chaining.
     */
    render() {
        this.$el
            .html(this.template(this.model.attributes))
            .toggleClass('checked', this.model.get('checked'));

        return this;
    },

    /**
     * Toggle the status of the checklist item.
     */
    _onToggleClicked() {
        this.model.toggle();
        this.$el.toggleClass('checked', this.model.get('checked'));
    },

    /**
     * Switch the item into edit mode.
     */
    _startEdit() {
        if (!this.$el.hasClass('editing')) {
            this.$el.toggleClass('editing');

            this.$('.checklist-item-description')
                .prop('contenteditable', true)
                .focus()
                .select();
        }
    },

    /**
     * Respond to user input in the editor.
     *
     * Update the description of the checklist item on enter key press.
     * Cancel editing on escape key press.
     *
     * Args:
     *     ev (Event):
     *         The event that triggered the action.
     */
    _onEditKeyDown(ev) {
        if (ev.keyCode === $.ui.keyCode.ENTER || ev.keyCode === 13) {
            // Enter confirms the edit.
            ev.preventDefault();
            ev.stopPropagation();

            this._confirmEdit();
        } else if (ev.keyCode === $.ui.keyCode.ESCAPE || ev.keyCode === 27) {
            // Escape cancels the edit.
            ev.preventDefault();
            ev.stopPropagation();

            this._cancelEdit();
        } else if (ev.altKey || ev.ctrlKey || ev.metaKey) {
            /*
             * Prevent any kind of special modifiers (such
             * bolding or italicizing).
             */
            ev.preventDefault();
            ev.stopPropagation();
        }
    },

    /**
     * Accept the edited text.
     */
    _confirmEdit() {
        const description = this.$('.checklist-item-description').text().trim();

        if (description !== '') {
            this.model.updateDescription(description);
            this._endEdit();
        }
    },

    /**
     * Cancel the edit.
     */
    _cancelEdit() {
        this._endEdit();

        this.$('.checklist-item-description')
            .text(this.model.get('description'));
    },

    /**
     * Finish the edit operation.
     */
    _endEdit() {
        this.$el.toggleClass('editing');
        this.$('.checklist-item-description')
            .prop('contenteditable', false);
    },

    /**
     * Delete the item.
     */
    _onRemoveClicked() {
        this.model.remove();
    },
});


/**
 * The main checklist view, including header and new item input field.
 */
Checklist.ChecklistView = Backbone.View.extend({
    className: 'checklist',

    events: {
        'keyup input[name="checklist-add-item"]': '_onAddItemKeyUp',
        'click .checklist-toggle-size': '_toggleExpand',
    },

    checklistTemplate: _.template(dedent`
        <div class="checklist-header">
         <span class="checklist-title">✔ Checklist</span>
         <span class="rb-icon rb-icon-collapse checklist-toggle-size"></span>
        </div>
        <div class="checklist-body">
         <ul class="checklist-items"></ul>
         <div class="checklist-field">
          <input name="checklist-add-item" placeholder="Add a new item">
         </div>
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
     *     reviewRequestID (number):
     *         The ID of the current review request.
     */
    initialize(options) {
        this.collection = new Checklist.ChecklistItemCollection();
        this.listenTo(this.collection, 'add', this._addItemToView);

        this.checklist = new Checklist.Checklist();
        this.checklist.save({
            data: {
                review_request_id: options.reviewRequestID,
            },
            success: model => {
                // Ready the collection of checklist items.
                this.collection.checklistId = model.get('id');
                this.collection.fetch();

                this.render();
            },
        });
    },

    /**
     * Render the view.
     *
     * Returns:
     *     Checklist.ChecklistView:
     *     This object, for chaining.
     */
    render() {
        this.$el.html(this.checklistTemplate());
        this._$list = this.$('.checklist-items');

        return this;
    },

    /**
     * Add a new item to the view.
     *
     * Args:
     *     item (Checklist.ChecklistItem):
     *         The new item to add.
     */
    _addItemToView(item) {
        const itemView = new Checklist.ChecklistItemView({
            model: item,
        });
        itemView.$el.appendTo(this._$list);
    },

    /**
     * Handle a keyup event on the "Add a new item" input.
     *
     * Args:
     *     ev (Event):
     *         The keyboard event.
     */
    _onAddItemKeyUp(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        if (ev.keyCode === $.ui.keyCode.ENTER || ev.keyCode === 13) {
            const $input = this.$('input[name=checklist-add-item]');
            const description = $input.val().trim();

            if (description !== '') {
                $input.val('');

                this.collection.create({
                    description: description,
                });
            }
        }
    },

    /**
     * Toggle the checklist open or closed.
     */
    _toggleExpand() {
        this.$('.checklist-body').toggleClass('hidden');
        this.$('#checklist-toggle-size div')
            .toggleClass('rb-icon-expand')
            .toggleClass('rb-icon-collapse');
    },
});


}
