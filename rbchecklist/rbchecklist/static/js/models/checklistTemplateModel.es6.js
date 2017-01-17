/**
 * The template resource.
 */
Checklist.Template = RB.BaseResource.extend({
    rspNamespace: 'checklist_template',

    defaults: {
        title: null,
        items: []
    },

    /**
     * Parse the data from the server.
     *
     * This is a no-op.
     *
     * Args:
     *     response (object):
     *         The response from the server.
     *
     * Returns:
     *     object:
     *     The parsed data.
     */
    parse(response) {
        return response;
    },

    /**
     * Return the API url for this template.
     *
     * Returns:
     *     string:
     *     The URL for this template's API resource.
     */
    url() {
        const url = `${Checklist.API_PATH}checklist-templates/`;
        return this.isNew() ? url : (url + this.id + '/');
    },

    /**
     * Return a JSON-serializable representation of this object.
     *
     * Returns:
     *     object:
     *     The serializable form.
     */
    toJSON() {
        return {
            title: this.get('title') || undefined,
            items: JSON.stringify(this.get('items')) || undefined,
        };
    },

    /**
     * Save this template.
     *
     * This overrides the default behavior to unset the attributes if an error
     * occurs.
     *
     * Args:
     *     attributes (object):
     *         The new attributes to save.
     *
     *     options (object, optional):
     *         Options for the save operation.
     *
     *     context (object, optional):
     *         Context to use when calling callbacks.
     */
    save(attributes, options={}, context=undefined) {
        const oldAttributes = _.clone(this.attributes);

        this.set({
            title: attributes.title,
            items: attributes.items,
        });

        _.extend(options, {
            wait: true,
            success: (model, response) => {
                this.set(response.checklist_template);
                this.trigger('update');
            },
            error: () => {
                this.set(oldAttributes);
                this.trigger('show');
            },
        });

        RB.BaseResource.prototype.save.call(this, options, context);
    }
});


/**
 * A collection of templates.
 */
Checklist.TemplateCollection = RB.BaseCollection.extend({
    model: Checklist.Template,

    /**
     * Parse the response from the server and return the data.
     *
     * Args:
     *     response (object):
     *          The data returned by the server.
     *
     * Returns:
     *     object:
     *     The parsed response.
     */
    parse(response) {
        return response.checklist_templates;
    },

    /**
     * Return the API url for this collection.
     *
     * Returns:
     *     string:
     *     The URL for this collection's API resource.
     */
    url() {
        return `${Checklist.API_PATH}checklist-templates/`;
    }
});
