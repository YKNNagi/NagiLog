from django import template
from django.utils.safestring import mark_safe

from ..markdown import render_markdown, render_markdown_summary


register = template.Library()


@register.filter
def markdown(value):
    safe_html = render_markdown(value)

    return mark_safe(safe_html)

@register.filter
def markdown_summary(value):
    return render_markdown_summary(value)