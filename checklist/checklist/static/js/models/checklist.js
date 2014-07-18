/* A checklist is a collection of checklist items.
 * A checklistItem is an individual item in a checklist. */
var Checklist = {};

Checklist.ChecklistItem = Backbone.Model.extend({
    defaults: {
        description: '',
        id: '',
        finished: false
    }
});

Checklist.Checklist = Backbone.Collection.extend({
    model: Checklist.ChecklistItem
});