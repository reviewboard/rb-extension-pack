/**
 * Provides review capabilities for XML files.
 */
RB.XMLReviewable = RB.FileAttachmentReviewable.extend({
    commentBlockModel: RB.FileAttachmentCommentBlock,

    defaults: _.defaults({
        xmlContent: '',
    }, RB.FileAttachmentReviewable.prototype.defaults),
});
