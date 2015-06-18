__author__ = 'joel'
from django import template

register = template.Library()

from angular.version import get_version

@register.simple_tag()
def version_extension():
    return '?v=' + get_version()
