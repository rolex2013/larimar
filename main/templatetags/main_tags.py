from django import template  
from main.models import Menu, MenuItem
from companies.models import UserCompanyComponentGroup
from django.db.models import Q #, Count, Min, Max, Sum, Avg 
from django.contrib import auth
#import requests
  
  
register = template.Library() 

@register.simple_tag(takes_context=True)
def left_menu(context, menuid=0, is_auth=False):
    #group_name = ''
    if is_auth == True:
       #group = UserCompanyComponentGroup.objects.get(user_id=context.request.user, company_id=, component_id='1').order_by('-group_id')
       if menuid == 0:
          nodes = MenuItem.objects.filter(Q(menu_id=2) & Q(is_active=True) & (Q(component_id__in=context.request.session['_auth_user_component_id']) | Q(component_id__in=[]) | Q(component_id=1)))   # Главное (левое) меню
       else:
          nodes = MenuItem.objects.filter(Q(menu_id=menuid) & Q(is_active=True) & (Q(component_id__in=context.request.session['_auth_user_component_id']) | Q(component_id=None)))  
    else:
       nodes = MenuItem.objects.filter(menu_id=1, is_active=True)
    #return (nodes.order_by())
    return (nodes)

@register.simple_tag(takes_context=True)
def group_name(context, is_auth=False):
    groupname = ''
    if is_auth == True:
       try:
          uccg = UserCompanyComponentGroup.objects.filter(user_id=context.request.user, component_id='1').order_by('-group_id')[0]
          groupname = '"'+uccg.group.name+'"'
       except:
          groupname = '"Не назначено"'         
    return (groupname)

@register.inclusion_tag('left_menu.html', takes_context=True)
def left__menu(context):
    return {
        'link': 'kjkjkjkjkj============',
        'title': ';lkl;klklkl kljkjkjk===',
        'cnt': 5
    }         