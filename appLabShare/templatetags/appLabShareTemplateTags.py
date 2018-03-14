from django import template


register = template.Library()


@register.filter
def getItem (contextDict, key):
    return contextDict.get(key)