RB.PageManager.ready(page => {
    const view = new Checklist.ChecklistView({
        reviewRequestID: page.reviewRequest.id,
    });

    view.render();
    view.$el.appendTo(document.body);
});
