{


/**
 * The view for each item on the checklist.
 */
Checklist.ChecklistItemView = Backbone.View.extend({
    tagName: 'li',
    className: 'checklist-item',

    events: {
        'click input[name="checklist-checkbox"]': '_onToggleClicked',
        'click div.checklist-item-edit': '_onEditClicked',
        'keyup input[name="checklist-edit-description"]': '_onItemEditorChanged',
        'click div.checklist-item-edit-cancel': '_onCancelEditClicked',
        'click div.checklist-item-delete': '_onRemoveClicked',
    },

    /**
     * The template for items in their default state.
     */
    template: _.template(dedent`
        <div class="checklist-item-checkbox">
         <input type="checkbox" name="checklist-checkbox"
                <% if (checked) { %> checked="checked" <% } %> >
        </div>
        <div class="checklist-item-desc">
         <%- description %>
        </div>
        <div class="checklist-item-actions">
         <div class="checklist-item-edit">
          <span class="rb-icon rb-icon-edit"></span>
         </div>
         <div class="checklist-item-delete">
          <span class="rb-icon rb-icon-delete"></span>
         </div>
        </div>
    `),

    /**
     * The view template when editing an item.
     */
    edit_template: _.template(dedent`
        <input type="checkbox" name="checklist-checkbox"
               <% if (checked) { %> checked="checked" <% } %> >
        <input name="checklist-edit-description" value="<%- description %>">
        <div class="checklist-item-actions">
         <div class="checklist-item-edit-cancel">
          <span class="rb-icon rb-icon-delete"></span>
         </div>
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
        this.$el.html(this.template(this.model.attributes));
        return this;
    },

    /**
     * Toggle the status of the checklist item.
     *
     * Args:
     *     ev (Event):
     *         The event that triggered the action.
     */
    _onToggleClicked(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        this.model.toggle();
    },

    /**
     * Switch the item into edit mode.
     *
     * Args:
     *     ev (Event):
     *         The event that triggered the action.
     */
    _onEditClicked(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        this.$el
            .html(this.edit_template(this.model.attributes))
            .children('input[name=checklist-edit-description]')
                .select();
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
    _onItemEditorChanged(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        if (ev.keyCode === $.ui.keyCode.ENTER || ev.keyCode === 13) {
            const $input = this.$('input[name=checklist-edit-description]');
            const description = $input.val().trim();

            if (description !== '') {
                this.model.updateDescription(description);
            }
        } else if (ev.keyCode === $.ui.keyCode.ESCAPE ||
                   ev.keyCode === 27) {
            this._onCancelEditClicked();
        }
    },

    /**
     * Cancel the edit operation.
     */
    _onCancelEditClicked() {
        this.$el.html(this.template(this.model.attributes));
    },

    /**
     * Delete the item.
     *
     * Args:
     *     ev (Event):
     *         The event that triggered the action.
     */
    _onRemoveClicked(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        this.model.remove();
    },
});


/**
 * The main checklist view, including header and new item input field.
 */
Checklist.ChecklistView = Backbone.View.extend({
    id: 'checklist',
    className: 'checklist',

    events: {
        'keyup input[name="checklist-add-item"]': '_onAddItemKeyUp',
        'click div#checklist-toggle-size': '_toggleExpand',
    },

    checklistTemplate: _.template(dedent`
        <div class="checklist-box">
         <div class="checklist-header">
          <div class="checklist-title">Checklist</div>
          <div id="checklist-toggle-size">
           <div class="rb-icon rb-icon-collapse"></div>
          </div>
         </div>
         <div id="checklist-body">
          <ul class="checklist-items"></ul>
          <div class="checklist-field">
           <input name="checklist-add-item"
                  placeholder="Add a new item"/>
          </div>
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
        this.$('#checklist-body').toggleClass('hidden');
        this.$('#checklist-toggle-size div')
            .toggleClass('rb-icon-expand')
            .toggleClass('rb-icon-collapse');
    },
});


}
