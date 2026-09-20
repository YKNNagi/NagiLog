import bleach
import markdown
from django.utils.html import strip_tags


ALLOWED_TAGS = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "strong",
    "em",
    "ul",
    "ol",
    "li",
    "blockquote",
    "code",
    "pre",
    "a",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href"],
}

ALLOWED_PROTOCOLS = [
    "http",
    "https",
]

def render_markdown(text):
    html = markdown.markdown(text)

    safe_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )

    return safe_html

def render_markdown_summary(text):
    safe_html = render_markdown(text)
    plain_text = strip_tags(safe_html)
    summary = " ".join(plain_text.split())

    return summary