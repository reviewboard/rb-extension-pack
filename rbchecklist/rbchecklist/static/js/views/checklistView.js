(function() {


/*
 * The view for each item on the checklist.
 */
Checklist.ChecklistItemView = Backbone.View.extend({
    tagName: 'li',
    className: 'checklist-item',

    events: {
        'click input[name="checklist-checkbox"]': 'toggleStatus',
        'click div.checklist-item-edit': 'switchToEditView',
        'keydown input[name="checklist-edit-description"]': 'editItem',
        'click div.checklist-item-edit-cancel': 'editItemCancel',
        'click div.checklist-item-delete': 'removeItem',
    },

    /* This tempate is for the default look of a checklist item. */
    template: _.template([
        '<div class="checklist-item-checkbox">',
        ' <input type="checkbox" name="checklist-checkbox" ',
        '  <% if (checked) { %> checked="checked" <% } %> >',
        '</div>',
        '<div class="checklist-item-desc">',
        ' <%- description %>',
        '</div>',
        '<div class="checklist-item-actions">',
        ' <div class="checklist-item-edit">',
        '  <span class="rb-icon rb-icon-edit"></span>',
        ' </div>',
        ' <div class="checklist-item-delete">',
        '  <span class="rb-icon rb-icon-delete"></span>',
        ' </div>',
        '</div>'
    ].join('')),

    /* The view template when editing a checklist item. */
    edit_template: _.template([
        '<input type="checkbox" name="checklist-checkbox" ',
        ' <% if (checked) { %> checked="checked" <% } %> >',
        '<input name="checklist-edit-description" value="<%- description %>">',
        '</input>',
        '<div class="checklist-item-actions">',
        ' <div class="checklist-item-edit-cancel">',
        '  <span class="rb-icon rb-icon-delete"></span>',
        ' </div>',
        '</div>'
    ].join('')),

    initialize: function(options) {
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destroy', this.remove);

        this.render();
    },

    render: function() {
        this.$el.html(this.template(this.model.attributes));
        return this;
    },

    /* Toggle the status of the checklist item. */
    toggleStatus: function(event) {
        event.preventDefault();
        this.model.toggle();
        return false;
    },

    /*
     * Edit button click handler.
     *
     * Render the edit view template and selects the input field for
     * editing.
     */
    switchToEditView: function(event) {
        event.stopPropagation();

        this.$el.html(this.edit_template(this.model.attributes));
        this.$el.children('input[name=checklist-edit-description]').select();

        return false;
    },

    /*
     * Edit input field handler.
     *
     * Update the description of the checklist item on enter key press.
     * Cancel editing on escape key press.
     */
    editItem: function(event) {
        var description, $input;

        if (event.keyCode === $.ui.keyCode.ENTER || event.keyCode === 13) {
            $input = this.$el.find('input[name=checklist-edit-description]');
            description = $input.val().trim();

            if (description === '') {
                alert("Please type a description");
                return;
            }

            this.model.updateDescription(description);
        } else if (event.keyCode === $.ui.keyCode.ESCAPE ||
                   event.keyCode === 27) {
            this.editItemCancel();
        }
    },

    /* Cancel button click handler. (same icon as delete) */
    editItemCancel: function() {
        this.$el.html(this.template(this.model.attributes));
    },

    /* Delete button click handler. */
    removeItem: function(event) {
        event.preventDefault();
        this.model.remove();
        return false;
    }
});


/*
 * The main checklist view, including header and new item input field.
 */
Checklist.ChecklistView = Backbone.View.extend({
    id: 'checklist',
    className: 'checklist',

    events: {
        'keydown input[name="checklist-add-item"]': 'addItem',
        'click div#checklist-toggle-size': 'toggleViewSize'
    },

    checklistTemplate: _.template([
        '<div class="checklist-box">',
        ' <div class="checklist-header">',
        '  <div class="checklist-title">Checklist</div>',
        '  <div id="checklist-toggle-size">',
        '   <div class="rb-icon rb-icon-collapse"></div>',
        '  </div>',
        ' </div>',
        ' <div id="checklist-body">',
        '  <ul class="checklist-items"></ul>',
        '  <div class="checklist-field">',
        '   <input name="checklist-add-item" ',
        '          placeholder="Add a new item"/>',
        '  </div>',
        ' </div>',
        '</div>'
    ].join('')),

    initialize: function(options) {
        this.collection = new Checklist.ChecklistItemCollection();
        this.listenTo(this.collection, 'add', this._addItemToView);

        this.checklist = new Checklist.Checklist();
        this.checklist.save({
            data: {
                review_request_id: options.reviewRequestID
            },
            success: _.bind(function(model, response) {
                // Ready the collection of checklist items.
                this.collection.checklistId = model.get('id');
                this.collection.fetch();

                this.render();
            }, this)
        }, this);
    },

    /* Render the checklist on the page. */
    render: function() {
        this.$el.html(this.checklistTemplate());
        this._$list = this.$el.find('ul.checklist-items');
    },

    /* Append item to the view when an item is added to the checklist. */
    _addItemToView: function(item) {
        var itemView = new Checklist.ChecklistItemView({
            model: item
        });
        itemView.$el.appendTo(this._$list);
    },

    /* Add a new item. */
    addItem: function(event) {
        var $input, description, item;

        if (event.keyCode === $.ui.keyCode.ENTER || event.keyCode === 13) {
            $input = this.$('input[name=checklist-add-item]');
            description = $input.val().trim();
            $input.val('');

            if (description === '') {
                alert("Please type a description");
                return;
            }

            this.collection.create({
                description: description
            });
        }
    },

    /* Handler for toggling the checklist box. */
    toggleViewSize: function() {
        $('#checklist-body').toggleClass('hidden');
        $('#checklist-toggle-size div').toggleClass('rb-icon-expand');
        $('#checklist-toggle-size div').toggleClass('rb-icon-collapse');
    }
});


/*
 * For the instantiation method in the html page.
 */
Checklist.Extension = RB.Extension.extend();


})();
