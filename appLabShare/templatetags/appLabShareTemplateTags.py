from django import template


register = template.Library()

@register.inclusion_tag("labShare/enrol.html")
@register.filter
def getItem (dictionary, key):
    return dictionary.get(key)