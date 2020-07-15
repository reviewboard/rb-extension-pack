/**
 * Displays a review UI for XML files.
 */
RB.XMLReviewableView = RB.FileAttachmentReviewableView.extend({
    className: 'xml-review-ui',

    /**
     * Render the view content.
     *
     * Returns:
     *     RB.XMLReviewableView:
     *     This object, for chaining.
     */
    renderContent: function() {
        this.$el.html(this.model.get('xmlContent'));

        return this;
    },
});
