from django import template

register = template.Library()

@register.filter
def is_pending(value):
    return value == 'Pending'