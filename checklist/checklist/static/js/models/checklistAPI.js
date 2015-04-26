/* An API for the Checklist Extension. */
Checklist.ChecklistAPI = RB.BaseResource.extend({
    rspNamespace: 'checklist',
    checklist_items: null,

    defaults: {
        /* The id of the user interacting with the Checklist. */
        user_id: null,

        /* The id of the review request the checklist is for. */
        review_request_id: null,

        /* The item in the checklist being modified / deleted. */
        checklist_item_id: null,

        /* The description for the indicated checklist item. */
        item_description: null,

        /* Indicates whether the checklist item's status should be toggled. */
        toggle: false
    },

    url: function () {
        var baseURL = SITE_ROOT + 'api/extensions/checklist.extension.Checklist/checklists/';
        return this.isNew() ? baseURL : (baseURL + this.id + '/');
    },

    toJSON: function () {
        return {
            /*
             * If this.get('attribute') is null, it will be undefined and
             * not sent to the server.
             */
            user_id: this.get('user_id') || undefined,
            review_request_id: this.get('review_request_id') || undefined,
            checklist_item_id: this.get('checklist_item_id') || undefined,
            item_description: this.get('item_description') || undefined,
            toggle: this.get('toggle') || undefined
        };
    },

    parseResourceData: function(rsp) {
        this.checklist_items = rsp.checklist_items;
        return {
            id: rsp.id,
            links: rsp.links,
            checklist_item_id: rsp.items_counter,
            loaded: true
        };
    }
});
