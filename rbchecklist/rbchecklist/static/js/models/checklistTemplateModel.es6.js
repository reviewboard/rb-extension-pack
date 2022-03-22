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
     * Returns:
     *     Promise:
     *     A promise which resolves when the operation is complete.
     */
    async save(attributes) {
        const oldAttributes = _.clone(this.attributes);

        this.set({
            title: attributes.title,
            items: attributes.items,
        });

        try {
            const rsp = await RB.BaseResource.prototype.save.call(this);
            this.set(rsp.checklist_template);
            this.trigger('update');
        } catch (err) {
            this.set(oldAttributes);
            this.trigger('show');
        }
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
