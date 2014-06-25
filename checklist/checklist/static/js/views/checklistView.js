/* A view for each item on the checklist. */
Checklist.ChecklistItemView = Backbone.View.extend({
    tagName: 'li',
    className: 'checklist_item',

    /* We pass in the checklistAPI as an argument so that each item has
     * access to the API also. */

    events: {
        'click input[name="checklist_checkbox"]': 'toggleStatus',
        'click a.checklist_edit_desc': 'editItemDesc',
        'keydown input[name="checklist_editDesc"]': 'editItemDescDB'
    },

    initialize: function(options) {
        _.bindAll(this, 'render', 'toggleStatus', 'toggleStatusDB');
        this.checklistAPI = options.checklistAPI;
        this.listenTo(this.model, 'change', this.render);
    },

    /* This tempate is for the regular look of an item. */
    template: _.template([
        '<input type="checkbox" name="checklist_checkbox" ',
        '<% if (finished) { %> checked="checked" <% } %> >',
        '<a class="checklist_edit_desc" href="#" size="5"><%= description %></a>',
        '<a id=<%= id %> class="checklist_del_item" href="#">X</a>'
    ].join('')),

    render: function() {
        this.$el.attr('id', 'checklist_item' + this.model.get("id"));
        this.$el.html(this.template(this.model.attributes));
        return this;
    },

    /* Toggle the status of the Backbone object on the front-end. */
    toggleStatus: function() {
        this.model.set({
            finished: !this.model.get("finished")
        });

        this.toggleStatusDB();
    },

    /* Toggle the status of the item on the back-end. */
    toggleStatusDB: function() {
        var item_id = this.model.get("id");
        this.checklistAPI.set({
            toggle: true,
            checklist_item_id: item_id,
            item_description: null
        });

        this.checklistAPI.save(null, this);
    },

    /* This template is for the textfield that allows the user to edit
     * the item description. */
    edit_template: _.template([
        '<input type="checkbox" name="checklist_checkbox" ',
        '<% if (finished) { %> checked="checked" <% } %> >',
        '<input name="checklist_editDesc" value="<%= description %>"</input>',
        '<a id=<%= id %> class="checklist_del_item" href="#">X</a>'
    ].join('')),

    /* When an item is clicked, a textfield should show up. */
    editItemDesc: function(event) {
        event.stopPropagation();
        this.$el.html(this.edit_template(this.model.attributes));

        return false;
    },

    /* When the user presses enter on the textfield, the form should be
     * submitted to the back-end. */
    editItemDescDB: function(event) {
        if (event.keyCode === 13) {
            item_desc = $('input[name=checklist_editDesc]').val();

            this.checklistAPI.set({
                item_description: item_desc,
                checklist_item_id: this.model.get("id")
            });

            var saveOptions = {
                success: function(data) {
                    /* Update the Backbone model's description. */
                    this.model.set({
                        description: item_desc
                    });
                    this.$el.html(this.template(this.model.attributes));
                }
            };

            this.checklistAPI.save(saveOptions, this);

            return false;
        }
    }

});

Checklist.ChecklistView = Backbone.View.extend({
    events: {
        'keydown input[name="checklist_item_description"]': 'addItemDB',
        'click a.checklist_del_item': 'removeItem',
        'click a#checklist_toggle_size': 'toggleViewSize',
        'click a#checklist_exit': 'deleteChecklist',
        'click a#checklist_clear': 'clearItemInput'
    },

    initialize: function(options) {
        /* Bind every function that uses 'this' as current object. */
        _.bindAll(this, 'render', 'addItemDB', 'addItem', 'appendItem',
                  'removeItemDB', 'removeItem', 'toggleViewSize',
                  'createNewChecklist', 'deleteChecklist');

        this.review_request_id = options.review_request_id;
        this.user_id = options.user_id;

        this.checklistAPI = new Checklist.ChecklistAPI();
        this.savedHeight = 0;
        this.isMinimized = false;
        this.CHECKLIST_MINIMIZED_HEIGHT = 25;

        /* Create a new checklist. */
        this.collection = new Checklist.Checklist();
        this.collection.bind('add', this.appendItem);
        this.createNewChecklist();
    },

    /* Create or GET a checklist on the server side. Let the API handle
    this one. */
    createNewChecklist: function() {
        this.checklistAPI.set({
            user_id: this.user_id,
            review_request_id: this.review_request_id,
        });

        var self = this;
        var saveOptions = {
            success: function(data) {
                this.render();
                /* The checklist we receive from the back-end may not be empty,
                   so we need to add the items it already has to the collection. */
                $.each(self.checklistAPI.checklist_items, function (ind, item) {
                    self.addItem(item.id, item.description, item.finished);
                });
            }
        };

        this.checklistAPI.save(saveOptions, this);
    },

    checklistTemplate: _.template([
        '<div class="checklist_box" id="checklist">',
        ' <div class="checklist_header">',
        '  <div class="checklist_title">Checklist</div>',
        '  <div class="checklist_actions">',
        '   <ul class="checklist_header_btn">',
        '    <li><a id="checklist_toggle_size">Min</a></li>',
        '    <li><a id="checklist_exit">Close</a></li>',
        '   </ul>',
        '  </div>',
        ' </div>',
        ' <div class="checklist_body">',
        '  <ul class="checklist_items"></ul>',
        ' </div>',
        ' <div class="checklist_footer">',
        '  <input name="checklist_item_description" ',
        '         placeholder="Add a new item"/>',
        '  <a id="checklist_clear" href="#">X</a>',
        ' </div>',
        '</div>'
    ].join('')),

    /* Render the checklist on the page. */
    render: function() {
        this.$el.html(this.checklistTemplate());
        this._$ul = this.$('ul.checklist_items');

        /* If collection is not empty, we want to render each item inside
         * it. */
        $(this.collection.models).each(function(item) {
            this.appendItem(item);
        }, this);

        $('#checklist').empty().append(this.$el);
    },

    /* Toggle between minimize and maximize the height */
    toggleViewSize: function() {
        var heightChange = 0,
            $checklistBox = this.$('.checklist_box'),
            $sizeTextToggle = this.$('#checklist_toggle_size');
        this.isMinimized = !this.isMinimized;

        if (this.isMinimized) {
            /* Minimize the view */
            $sizeTextToggle.text("Max");
            /* Narrow down the checklist. Remember the current height. */
            this.savedHeight = $checklistBox.height();
            heightChange = this.CHECKLIST_MINIMIZED_HEIGHT;

        } else {
            /* Maximize the view */
            $sizeTextToggle.text("Min");
            heightChange = this.savedHeight;
        }

        $checklistBox.animate({
            height: heightChange
        }, 400);

        this.$el.attr('overflow', 'hidden');
        return false;
    },

    /* Add the new item to the backend. */
    addItemDB: function(event) {
        if (event.keyCode === 13) {
            var $itemDescriptionInput = this.$('input[name=checklist_item_description]'),
                item_desc = $itemDescriptionInput.val();
            $itemDescriptionInput.val('');

            if (item_desc === '') {
                alert("Please type a description");
                return;
            }

            this.checklistAPI.set({
                item_description: item_desc,
                checklist_item_id: null
            });

            var self = this;
            var saveOptions = {
                success: function(data) {
                    var item_id = data.attributes.checklist_item_id;
                    self.addItem(item_id, item_desc, false);
                }
            };

            this.checklistAPI.save(saveOptions, this);
        }
    },

    /* Add the new item to the collection on the front end. */
    addItem: function(item_id, item_desc, status) {
        var item = new Checklist.ChecklistItem();
        item.set({
            description: item_desc,
            id: item_id,
            finished: status
        });

        this.collection.add(item);

        return false;
    },

    /* Create and render the new checklist item. */
    appendItem: function(item) {
        var self = this;
        var checklistItemView = new Checklist.ChecklistItemView({
            model: item,
            checklistAPI: self.checklistAPI
        });
        this._$ul.append(checklistItemView.render().el);

        return false;
    },

    /* First, find the item, and remove it from the models. */
    removeItem: function(e) {
        var id = $(e.currentTarget).attr("id"),
            item = this.collection.get(id);

        e.preventDefault();
        this.collection.remove(item);

        /* Then remove its view too. */
        $("#checklist_item" + id).remove();

        /* Then remove it from the database. */
        this.removeItemDB(id);

        return false;
    },

    removeItemDB: function(item_id) {
        this.checklistAPI.set({
            item_description: '',
            checklist_item_id: item_id,
            toggle: null
        });

        this.checklistAPI.save(null, this);
    },

    deleteChecklist: function() {
        var response = confirm("This action will delete the entire checklist." +
            "This cannot be undone.");

        if (response) {
            var saveOptions = {
                success: function(data) {
                    this.remove();
                }
            };
            this.checklistAPI.destroy(saveOptions, this);
        }

        return false;
    },

    /* Clear input text fiels */
    clearItemInput: function() {
        $('input[name=checklist_item_description]').val('');
    }
});

/* For the instantiation method in the html page. */
Checklist.Extension = RB.Extension.extend();