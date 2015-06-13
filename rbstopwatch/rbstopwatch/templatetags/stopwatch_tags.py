from __future__ import division, unicode_literals

from django import template
from django.utils.html import format_html
from django.utils.translation import ugettext as _


register = template.Library()


@register.filter
def review_time(review):
    if review.extra_data and 'rbstopwatch.reviewTime' in review.extra_data:
        totalSeconds = int(review.extra_data['rbstopwatch.reviewTime'])

        hours = totalSeconds // 3600
        minutes = (totalSeconds % 3600) // 60
        seconds = (totalSeconds % 60)

        time = '%02d:%02d:%02d' % (hours, minutes, seconds)

        return format_html(
            '<div class="rbstopwatch-review-header">{0}</div>',
            _('Total time spent on this review: %s') % time)

    return ''
