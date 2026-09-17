from django import template
from django.utils.safestring import mark_safe

from ..markdown import render_markdown


register = template.Library()


@register.filter
def markdown(value):
    safe_html = render_markdown(value)

    return mark_safe(safe_html)