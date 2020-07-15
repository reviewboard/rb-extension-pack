/**
 * Provides review capabilities for XML files.
 */
RB.XMLReviewable = RB.FileAttachmentReviewable.extend({
    defaults: _.defaults({
        xmlContent: '',
    }, RB.FileAttachmentReviewable.prototype.defaults),
});
