/* A view for each item on the checklist. */
Checklist.ChecklistItemView = Backbone.View.extend({
    tagName: 'li',
    className: 'checklist-item',

    events: {
        'click input[name="checklist_checkbox"]': 'toggleStatus',
        'click div.checklist-item-edit': 'editItemDesc',
        'keydown input[name="checklist_edit_description"]': 'editItemDescDB',
        'click div.checklist-item-edit-cancel': 'editItemCancel',
        'click div.checklist-item-delete': 'removeItem',
    },

    /* This tempate is for the regular look of an item. */
    template: _.template([
        '<div class="checklist-item-checkbox">',
        ' <input type="checkbox" name="checklist_checkbox" ',
        '  <% if (finished) { %> checked="checked" <% } %> >',
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

    /*
     * This template is for the textfield that allows the user to edit
     * the item description.
     */
    edit_template: _.template([
        '<input type="checkbox" name="checklist_checkbox" ',
        ' <% if (finished) { %> checked="checked" <% } %> >',
        '<input name="checklist_edit_description" value="<%- description %>">',
        '</input>',
        '<div class="checklist-item-actions">',
        ' <div class="checklist-item-edit-cancel">',
        '  <span class="rb-icon rb-icon-delete"></span>',
        ' </div>',
        '</div>'
    ].join('')),

    initialize: function(options) {
        // model from options attaches to the view.

        _.bindAll(this, 'render', 'toggleStatus', 'toggleStatusDB');

        /*
         * We pass in the checklistAPI as an argument so that each
         * item has access to the API also.
         */
        this.checklistAPI = options.checklistAPI;

        this.listenTo(this.model, 'change', this.render);
    },

    render: function() {
        this.$el.html(this.template(this.model.attributes));
        return this;
    },

    /* Toggle the status of the Backbone object on the front-end. */
    toggleStatus: function() {
        this.model.set({
            finished: !this.model.get('finished')
        });

        this.toggleStatusDB();
    },

    /* Toggle the status of the item on the back-end. */
    toggleStatusDB: function() {
        this.checklistAPI.set({
            toggle: true,
            checklist_item_id: this.model.get('id'),
            item_description: null
        });

        this.checklistAPI.save(null, this);
    },

    /* When an item is clicked, a textfield should show up. */
    editItemDesc: function(event) {
        event.stopPropagation();
        this.$el.html(this.edit_template(this.model.attributes));
        this.$el.children('input[name=checklist_edit_description]').select();

        return false;
    },

    /*
     * When the user presses enter on the textfield, the form should be
     * submitted to the back-end.
     */
    editItemDescDB: function(event) {
        var itemDesc, $input;

        if (event.keyCode === $.ui.keyCode.ENTER || event.keyCode === 13) {
            $input = this.$el.children('input[name=checklist_edit_description]');
            itemDesc = $input.val().trim();

            if (itemDesc === '') {
                alert("Please type a description");
                return;
            }

            this.checklistAPI.set({
                item_description: itemDesc,
                checklist_item_id: this.model.get('id')
            });

            this.checklistAPI.save({
                success: function(data) {
                    /* Update the Backbone model's description. */
                    this.model.set({
                        description: itemDesc
                    });
                    this.$el.html(this.template(this.model.attributes));
                }
            }, this);
        } else if (event.keyCode === $.ui.keyCode.ESCAPE ||
                   event.keyCode === 27) {
            this.editItemCancel();
        }
    },

    /* Cancels editing of the item description. */
    editItemCancel: function() {
        this.$el.html(this.template(this.model.attributes));
    },

    /* First, find the item, and remove it from the models. */
    removeItem: function(event) {
        event.preventDefault();
        this.model.collection.remove(this.model);

        /* Then remove it from the database. */
        this.removeItemDB();

        /* Then remove its view too. */
        this.remove();

        return false;
    },

    removeItemDB: function() {
        this.checklistAPI.set({
            item_description: '',
            checklist_item_id: this.model.get('id'),
            toggle: null
        });

        this.checklistAPI.save(null, this);
    }

});

Checklist.ChecklistView = Backbone.View.extend({
    events: {
        'keydown input[name="checklist_item_description"]': 'addItemDB',
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
        '   <input name="checklist_item_description" ',
        '          placeholder="Add a new item"/>',
        '  </div>',
        ' </div>',
        '</div>'
    ].join('')),

    initialize: function(options) {
        /* Bind every function that uses 'this' as current object. */
        _.bindAll(this, 'render', 'addItemDB', 'addItem', 'appendItem',
                  'createNewChecklist');

        this.review_request_id = options.review_request_id;
        this.user_id = options.user_id;

        this.checklistAPI = new Checklist.ChecklistAPI();

        /* Create a new checklist. */
        this.collection = new Checklist.Checklist();
        this.collection.bind('add', this.appendItem);
        this.createNewChecklist();
    },

    /*
     * Create or GET a checklist on the server side. Let the API handle
     * this one.
     */
    createNewChecklist: function() {
        var self = this;

        this.checklistAPI.set({
            user_id: this.user_id,
            review_request_id: this.review_request_id
        });

        this.checklistAPI.save({
            success: function(data) {
                this.render();
                /*
                 * The checklist we receive from the back-end may not be empty,
                 * so we need to add the items it already has to the collection.
                 */
                $.each(self.checklistAPI.checklist_items,
                       function(index, item) {
                    self.addItem(item.id, item.description, item.finished);
                });
            }
        }, this);
    },

    /* Render the checklist on the page. */
    render: function() {
        this.$el.html(this.checklistTemplate());
        this._$ul = this.$('ul.checklist-items');

        /* If collection is not empty, we want to render each item inside
         * it. */
        $(this.collection.models).each(function(item) {
            this.appendItem(item);
        }, this);

        $('#checklist').empty().append(this.$el);
    },

    /* Add the new item to the backend. */
    addItemDB: function(event) {
        var self = this,
            $input,
            itemDesc;

        if (event.keyCode === $.ui.keyCode.ENTER || event.keyCode === 13) {
            $input = this.$('input[name=checklist_item_description]');
            itemDesc = $input.val().trim();
            $input.val('');

            if (itemDesc === '') {
                alert("Please type a description");
                return;
            }

            this.checklistAPI.set({
                item_description: itemDesc,
                checklist_item_id: null
            });

            this.checklistAPI.save({
                success: function(data) {
                    var item_id = data.attributes.checklist_item_id;
                    self.addItem(item_id, itemDesc, false);
                }
            }, this);
        }
    },

    /* Add the new item to the collection on the front end. */
    addItem: function(item_id, itemDesc, status) {
        var item = new Checklist.ChecklistItem({
            description: itemDesc,
            id: item_id,
            finished: status
        });

        this.collection.add(item);

        return false;
    },

    /* Create and render the new checklist item. */
    appendItem: function(item) {
        var checklistItemView = new Checklist.ChecklistItemView({
                model: item,
                checklistAPI: this.checklistAPI
            });
        this._$ul.append(checklistItemView.render().el);

        return false;
    },

    /* Clear input text field. */
    clearItemInput: function() {
        $('input[name=checklist_item_description]').val('');
    },

    toggleViewSize: function() {
        $('#checklist-body').toggleClass('hidden');
        $('#checklist-toggle-size div').toggleClass('rb-icon-expand');
        $('#checklist-toggle-size div').toggleClass('rb-icon-collapse');
    }
});

/* For the instantiation method in the html page. */
Checklist.Extension = RB.Extension.extend();
