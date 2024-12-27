from core.forms import CommentForm
from django import template


register = template.Library()


@register.simple_tag()
def get_comment_form():
    form = CommentForm()
    return form
