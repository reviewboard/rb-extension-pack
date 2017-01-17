window.Checklist = {
    API_PATH: `${SITE_ROOT}api/extensions/rbchecklist.extension.Checklist/`,
};


/**
 * An individual checklist item contained in a checklist.
 *
 * There is no database model associated with this resource.
 */
Checklist.ChecklistItem = RB.BaseResource.extend({
    rspNamespace: 'checklist_item',

    defaults: {
        description: '',
        id: null,
        checked: false
    },

    /**
     * Return the API url for this item.
     *
     * Returns:
     *     string:
     *     The URL for this item's API resource.
     */
    url() {
        console.assert(this.collection !== null, 'collection must be set.');
        console.assert(this.collection.checklistId !== null,
                       'collection.checklistId must be set');

        const url = `${Checklist.API_PATH}checklists/${this.collection.checklistId}/checklist-items/`;
        return this.isNew() ? url : (url + this.id + '/');
    },

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
        if (response[this.rspNamespace]) {
            // If response is from individual checklist item API.
            return response[this.rspNamespace];
        } else {
            // If response is from checklist item collection.
            return response;
        }
    },

    /**
     * Return a JSON-serializable representation of this object.
     *
     * Returns:
     *     object:
     *     The serializable form.
     */
    toJSON() {
        return _.pick(this.attributes, 'checked', 'description');
    },

    /**
     * Update the description of the checklist item.
     *
     * Args:
     *     description (string):
     *         The new description.
     */
    updateDescription(description) {
        this.save({
            wait: true,
            data: {
                description: description,
            },
        });
    },

    /**
     * Toggle the checked state of the item and save.
     */
    toggle() {
        this.save({
            wait: true,
            data: {
                checked: !this.get('checked'),
            },
        });
    },

    /**
     * Remove and destroy the checklist item.
     */
    remove() {
        this.destroy({
            wait: true,
        });
    },
});


/**
 * A collection of checklist items.
 */
Checklist.ChecklistItemCollection = RB.BaseCollection.extend({
    model: Checklist.ChecklistItem,

    checklistId: null, // Used in this collection and the model.

    /**
     * Return the API url for this collection.
     *
     * Returns:
     *     string:
     *     The URL for this collection's API resource.
     */
    url() {
        console.assert(this.checklistId !== null, 'checklistId must be set');
        return `${Checklist.API_PATH}checklists/${this.checklistId}/checklist-items/`;
    },

    /**
     * Return the fetched checklist items.
     *
     * This maps an object that contains checklist items to an array of
     * checklist items after fetching, and maintains the order of the items.
     *
     * Args:
     *     response (object):
     *         The response from the server.
     *
     * Returns:
     *     array of object:
     *     The fetched items.
     */
    parse(response) {
        return _.values(response.checklist_item);
    },

    /**
     * Create a new item.
     *
     * This waits for a server response before adding it to the collection.
     *
     * Args:
     *     attrs (object):
     *         The attributes for the new item.
     */
    create(attrs) {
        const item = new Checklist.ChecklistItem(attrs, {
            collection: this,
        });

        item.save({
            success: model => this.add(model),
        });
    },
});


/**
 * The main checklist resource.
 *
 * This is used mainly to instantiate the collection of checklist items.
 */
Checklist.Checklist = RB.BaseResource.extend({
    rspNamespace: 'checklist',

    /**
     * Return the API url for this item.
     *
     * Returns:
     *     string:
     *     The URL for this item's API resource.
     */
    url() {
        const url = `${Checklist.API_PATH}checklists/`;
        return this.isNew() ? url : (url + this.id + '/');
    },

    /**
     * Parse the response from the server.
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
        return response[this.rspNamespace];
    },
});
