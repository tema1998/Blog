from django import template
from core.forms import CommentForm

register = template.Library()


@register.simple_tag()
def get_comment_form():
    form = CommentForm()
    return form
