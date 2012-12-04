/*
 * Displays a review UI for XML files.
 */
RB.XMLReviewableView = RB.FileAttachmentReviewableView.extend({
    className: 'xml-review-ui',

    /*
     * Renders the view.
     */
    renderContent: function() {
        this.$el.html(this.model.get('rendered'));

        return this;
    }
});
