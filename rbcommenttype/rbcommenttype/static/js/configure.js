$(function() {
    var Type,
        TypeView,
        TypeCollection,
        TypeCollectionView,
        $commentTypes = $('#id_types'),
        view;

    /*
     * A model representing a configured comment type.
     */
    Type = Backbone.Model.extend({
        defaults: {
            type: '',
            visible: true
        }
    });

    /*
     * A row in the configuration UI for a Type.
     */
    TypeView = Backbone.View.extend({
        tagName: 'tr',

        events: {
            'click #rbcommenttype-remove': '_remove',
            'change #rbcommenttype-visible': '_onVisibleChanged',
            'change #rbcommenttype-type': '_onTypeChanged'
        },

        template: _.template([
            '<td>',
            ' <input id="rbcommenttype-visible" type="checkbox"',
            '        <% if (visible) { %>checked<% } %>/>',
            '</td>',
            '<td>',
            ' <input id="rbcommenttype-type" value="<%- type %>"',
            '        size="40" />',
            '</td>',
            '<td>',
            ' <a href="#" id="rbcommenttype-remove">',
            '  <span class="rb-icon rb-icon-remove-widget"></span>',
            ' </a>',
            '</td>'
        ].join('')),

        /*
         * Render the type.
         */
        render: function() {
            this.$el.html(this.template(this.model.attributes));
            return this;
        },

        /*
         * Remove the type from the parent collection.
         */
        _remove: function() {
            this.model.destroy();
        },

        /*
         * Callback for when the visible checkbox is toggled. Updates the
         * model.
         */
        _onVisibleChanged: function(ev) {
            this.model.set('visible', $(ev.target).prop('checked'));
        },

        /*
         * Callback for when the type entry is changed. Updates the model.
         */
        _onTypeChanged: function(ev) {
            this.model.set('type', $(ev.target).val());
        }
    });

    /*
     * A collection of comment types.
     */
    TypeCollection = Backbone.Collection.extend({
        model: Type,

        /*
         * Initialize the collection from the existing JSON stored in the
         * <input> tag.
         */
        initialize: function(models, options) {
            this._$input = options.$input;
            this.add(JSON.parse(this._$input.val() || '[]'));

            this.listenTo(this, 'add remove change', this._onChange);
        },

        /*
         * Callback for when the collection changes. Updates the JSON stored in
         * the <input> tag.
         */
        _onChange: function() {
            this._$input.val(JSON.stringify(this));
        }
    });

    /*
     * A table showing all configured comment types.
     */
    TypeCollectionView = Backbone.View.extend({
        tagName: 'table',
        className: 'comment-types',

        template: _.template([
            '<thead>',
            ' <tr>',
            '  <td>Visible</td>',
            '  <td>Comment Type</td>',
            '  <td></td>',
            ' </tr>',
            '</thead>',
            '<tbody>',
            '</tbody>',
            '<tfoot>',
            ' <tr>',
            '  <td colspan="4">',
            '   <a href="#" id="rbcommenttype-add-type">Add type</a>',
            '  </td>',
            ' </tr>',
            '</tfoot>'
        ].join('')),

        events: {
            'click #rbcommenttype-add-type': '_addType'
        },

        /*
         * Initialize the view.
         */
        initialize: function() {
            this._views = [];
            this._rendered = false;

            _.bindAll(this, 'add', 'remove');

            this.collection.each(this.add);

            this.listenTo(this.collection, 'add', this.add);
            this.listenTo(this.collection, 'remove', this.remove);
        },

        /*
         * Add a row to the table.
         */
        add: function(type) {
            var view = new TypeView({model: type});
            this._views.push(view);

            if (this._rendered) {
                this.$('tbody').append(view.render().$el);
            }
        },

        /*
         * Remove a row from the table.
         */
        remove: function(type) {
            var view = _.select(this._views,
                                function(v) { return v.model == type; })[0];
            this._views = _.without(this._views, view);

            if (this._rendered) {
                view.$el.remove();
            }
        },

        /*
         * Render the table.
         */
        render: function() {
            var $tbody;

            this._rendered = true;
            this.$el.html(this.template());
            $tbody = this.$('tbody');

            _.each(this._views, function(view) {
                $tbody.append(view.render().$el);
            });
            return this;
        },

        /*
         * Internal helper to add a new type to the collection. This will end
         * up triggering the 'add' handler.
         */
        _addType: function() {
            this.collection.add(new Type());
            this._views[this._views.length - 1].$('input').focus();
            return false;
        }
    });

    view = new TypeCollectionView({
        collection: new TypeCollection(null, {
            $input: $commentTypes
        })
    });
    $commentTypes.after(view.render().$el);
});
