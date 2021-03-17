from django import template  
from main.models import Menu, MenuItem
from django.db.models import Q #, Count, Min, Max, Sum, Avg 
from django.contrib import auth
#import requests
  
  
register = template.Library() 

@register.simple_tag(takes_context=True)
def left_menu(context, menuid=0, is_auth=False):
    if is_auth == True:
       if menuid == 0:
          nodes = MenuItem.objects.filter(Q(menu_id=2) & Q(is_active=True) & (Q(component_id__in=context.request.session['_auth_user_component_id']) | Q(component_id__in=[])))   # Главное (левое) меню
       else:
          nodes = MenuItem.objects.filter(Q(menu_id=menuid) & Q(is_active=True) & (Q(component_id__in=context.request.session['_auth_user_component_id']) | Q(component_id=None)))  
    else:
       nodes = MenuItem.objects.filter(menu_id=1, is_active=True)
    return (nodes.order_by())

@register.inclusion_tag('left_menu.html', takes_context=True)
def left__menu(context):
    return {
        'link': 'kjkjkjkjkj============',
        'title': ';lkl;klklkl kljkjkjk===',
        'cnt': 5
    }         