from django import template  
from main.models import Menu, MenuItem
from companies.models import UserCompanyComponentGroup
from django.db.models import Q #, Count, Min, Max, Sum, Avg 
from django.contrib import auth
#import requests
from django.contrib.auth.models import User
from main.models import Notification
  
register = template.Library() 

@register.simple_tag(takes_context=True)
def left_menu(context, menuid=0, is_auth=False):
    #group_name = ''
    try:
        compid = context.request.session['_auth_user_component_id']
        if is_auth == True:
           #group = UserCompanyComponentGroup.objects.get(user_id=context.request.user, company_id=, component_id='1').order_by('-group_id')
           if menuid == 0:
              nodes = MenuItem.objects.filter(Q(menu_id=2) & Q(is_active=True) & (Q(component_id__in=compid) | Q(component_id__in=[]) | Q(component_id=1)))   # Главное (левое) меню
           else:
              nodes = MenuItem.objects.filter(Q(menu_id=menuid) & Q(is_active=True) & (Q(component_id__in=compid) | Q(component_id=None)))
        else:
           nodes = MenuItem.objects.filter(menu_id=1, is_active=True)
    except:
        nodes = MenuItem.objects.filter(menu_id=1, is_active=True)
        #print(nodes)
    return (nodes.order_by('sort'))
    #return (nodes)

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

# *** для вывода Уведомлений в SideBar'е ***

@register.simple_tag(takes_context=True)
def notifications(context, is_auth=False):

    nodes = []

    if is_auth == True:

        nodes = Notification.objects.filter(Q(author_id=context.request.user) | Q(recipient_id=context.request.user), is_active=True)

    return (nodes.order_by('datecreate'))

@register.simple_tag(takes_context=True)
def users_list(context, is_auth=False):

    users_list = []

    if is_auth == True:

        nodes = User.objects.filter(is_active=True)

    return (nodes.order_by('username'))