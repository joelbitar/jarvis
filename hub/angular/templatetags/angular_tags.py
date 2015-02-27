__author__ = 'joel'
from django import template
import re

register = template.Library()

@register.filter(name="ngvariable")
def csscolor(value):
    # Clean value.
    # If the value is not a typical hex value do not render # before
    return '{{ ' + value + ' }}'


@register.filter(name="addleft")
def addleft(value, argument):
    return argument + value
