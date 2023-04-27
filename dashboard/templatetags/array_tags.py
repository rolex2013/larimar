from django import template
register = template.Library()

@register.filter
def link(indexable, object_name):
    #print(indexable[object_name])
    return indexable.get(object_name)