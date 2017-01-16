(function() {


ChecklistTemplate = RB.BaseResource.extend({
    rspNamespace: 'checklist_template',

    defaults: {
        title: null,
        items: []
    },

    /* Simply return the model itself when there is incoming data. */
    parse: function(response) {
        return response;
    },

    /* URL for individual model operations with model id if not new. */
    url: function() {
        var url = SITE_ROOT + 'api/extensions/checklist.extension.Checklist/checklist-templates/';
        return this.isNew() ? url : (url + this.id + '/');
    },

    /* Map attributes to JSON to send to server. */
    toJSON: function () {
        return {
            title: this.get('title') || undefined,
            items: JSON.stringify(this.get('items')) || undefined
        };
    },

    /* Override save method to unset attributes on error. */
    save: function(attributes, options, context) {
        var oldAttributes = _.clone(this.attributes);
        options = options || {};

        this.set('title', attributes.title);
        this.set('items', attributes.items);

        _.extend(options, {
            wait: true,
            success: _.bind(function(model, response) {
                this.set(response.checklist_template);
                this.trigger('update');
            }, this),
            error: _.bind(function(model, response) {
                this.set(oldAttributes);
                this.trigger('show');
            }, this)
        });

        RB.BaseResource.prototype.save.call(this, options, context);
    }
});


ChecklistTemplateCollection = RB.BaseCollection.extend({
    model: ChecklistTemplate,

    /* Called after .fetch() to return models. */
    parse: function(response) {
        return response.checklist_templates;
    },

    /* URL for fetching list of models. */
    url: function() {
        return SITE_ROOT + 'api/extensions/checklist.extension.Checklist/checklist-templates/';
    }
});


})();
