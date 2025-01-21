from core.forms import CommentForm
from django import template


register = template.Library()


@register.simple_tag()
def get_comment_form():
    """
    Simple tag for getting form to write comment.
    """
    form = CommentForm()
    return form
