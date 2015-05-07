(function() {


/*
 * Namespace for the Checklist extension.
 */
Checklist = {
    apiPath: SITE_ROOT +
             'api/extensions/checklist.extension.Checklist/checklists/'
};


/*
 * Individual checklist item contained in a checklist.
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

    /*
     * Determine the url for a request.
     *
     * Uses the parent resource checklist's ID.
     */
    url: function() {
        var url;
        console.assert(this.collection !== null, 'collection must be set.');
        console.assert(this.collection.checklistId !== null,
                       'collection.checklistId must be set');
        url = Checklist.apiPath + this.collection.checklistId +
              '/checklist-items/';
        return this.isNew() ? url : (url + this.id + '/');
    },

    /* Return the checklist_item after fetching. */
    parse: function(response) {
        // If response is from individual checklist item API.
        if (response.checklist_item) {
            return response.checklist_item;
        }

        // If response is from checklist item collection.
        return response;
    },

    /* Convert attributes, if they exist, to JSON. */
    toJSON: function() {
        return {
            description: this.get('description') || undefined,
            checked: this.get('checked') || undefined
        }
    },

    /* Update the description of the checklist item. */
    updateDescription: function(description) {
        this.save({
            wait: true,
            data: {
                description: description
            }
        });
    },

    /* Toggle the checklist item between checked and unchecked, and save. */
    toggle: function() {
        this.save({
            wait: true,
            data: {
                checked: !this.get('checked')
            }
        });
    },

    /* Remove and destroy the checklist item. */
    remove: function() {
        this.destroy({
            wait: true
        });
    }
});


/*
 * Collection of checklist items.
 */
Checklist.ChecklistItemCollection = RB.BaseCollection.extend({
    model: Checklist.ChecklistItem,

    checklistId: null, // Used in this collection and the model.


    /*
     * Determine the url for a request.
     *
     * Uses the parent resource checklist's ID.
     */
    url: function() {
        console.assert(this.checklistId !== null, 'checklistId must be set');
        return Checklist.apiPath + this.checklistId +
               '/checklist-items/';
    },

    /*
     * Return fetched checklist items,
     *
     * This maps an object that contains checklist items to an array of
     * checklist items after fetching, and maintains the order of the items.
     */
    parse: function(response) {
        return _.values(response.checklist_item);
    },

    /*
     * Overridden create method to add a checklist item.
     *
     * This waits for a server response before adding it to the collection.
     */
    create: function(model) {
        // Initialize new checklist item model referencing this collection.
        var item = new Checklist.ChecklistItem(model, { collection: this });

        item.save({
            success: _.bind(function(model, response) {
                this.add(model);
            }, this)
        });
    }
});


/*
 * The main checklist resource.
 *
 * Used mainly to instantiate the collection of checklist items.
 */
Checklist.Checklist = RB.BaseResource.extend({
    rspNamespace: 'checklist',


    /* Determine the url for a checklist request. */
    url: function() {
        var url = Checklist.apiPath;
        return this.isNew() ? url : (url + this.id + '/');
    },

    /* Return fetched checklist object. */
    parse: function(response) {
        return response.checklist;
    }
});


})();
