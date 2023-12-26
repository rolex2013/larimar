from django import template
import datetime
from main.models import Menu, MenuItem, Meta_ObjectType
from companies.models import UserCompanyComponentGroup
from django.db.models import Q #, Count, Min, Max, Sum, Avg
from django.contrib import auth
#import requests
from django.contrib.auth.models import User
from main.models import Notification
from main.views import select_lang, notificationlist
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def left_menu(context, menuid=0, is_auth=False):
    # print(RequestContext)
    # print(request)
    # print('LANGUAGE_CODE:', settings.LANGUAGE_CODE, 'settings.LANGUAGE_SESSION_KEY:',
    #      settings.LANGUAGE_SESSION_KEY, 'settings.LANGUAGE_COOKIE_NAME:', settings.LANGUAGE_COOKIE_NAME)
    # select_lang(RequestContext)
    try:
        compid = context.request.session['_auth_user_component_id']
        if is_auth: # is True:
            # group = UserCompanyComponentGroup.objects.get(user_id=context.request.user, company_id=, component_id='1').order_by('-group_id')
            if menuid == 0:
                nodes = MenuItem.objects.filter(Q(menu_id=2) & Q(is_active=True) & (Q(component_id__in=compid) | Q(component_id__in=[]) | Q(component_id=1)))   # Главное (левое) меню
            else:
                nodes = MenuItem.objects.filter(Q(menu_id=menuid) & Q(is_active=True) & (Q(component_id__in=compid) | Q(component_id=None)))
        else:
            nodes = MenuItem.objects.filter(menu_id=1, is_active=True)
    except:
        nodes = MenuItem.objects.filter(menu_id=1, is_active=True)
        # print(nodes, context.request.session['_auth_user_component_id'])
    return (nodes.order_by('sort'))
    # return (nodes)


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
@register.inclusion_tag('sidebar_notifications_form.html', takes_context=True)
def notifications(context, is_auth=False):

    nodes = []

    if is_auth:
        # nodes = Notification.objects.filter(Q(author_id=context.request.user) | Q(recipient_id=context.request.user), type_id=3, is_read=False,
        #                                     is_active=True).select_related("author", "recipient", "objecttype").order_by('datecreate').distinct()
        nodes = notificationlist(context.request.user, '2', '0')
        # count = nodes.exclude(author_id=context.request.user.id).count()
        # count_unread = nodes.filter(is_read=False).count()
        count_unread = nodes.filter(
            Q(author=context.request.user, is_read_isauthor=False) | 
            Q(recipient=context.request.user, is_read_isrecipient=False)
        ).count()
        metaobjecttype_list = Meta_ObjectType.objects.filter(is_active=True).order_by("sort").distinct()

    return {
        'nodes':
        nodes.select_related("author", "recipient",
                             "objecttype").order_by('datecreate').distinct(),
        'status_selectid':
        "2",
        'metaobjecttype_list':
        metaobjecttype_list,
        'currentuserid':
        context.request.user.id,
        'count_unread':
        count_unread
    }

@register.simple_tag(takes_context=True)
def users_list(context, is_auth=False):
    #print('context = ', context)
    nodes = []

    if is_auth == True:

        members = list(set(list(UserCompanyComponentGroup.objects.filter(is_active=True, user__is_active=True, company__in=context.request.session[
            "_auth_user_companies_id"]).values_list('user_id', flat=True))))
        nodes = User.objects.filter(is_active=True, id__in=members).exclude(id=context.request.user.id).order_by('username').distinct()

    return (nodes)

@register.simple_tag(takes_context=False)
def copyright_show():

    copyright_text = '© 2017-' + str(datetime.datetime.now().year)
    designby_text = 'Designed by'
    designby_company = 'Larimar IT Group'
    designby_link = 'https://larimaritgroup.ru'
    hosting_company = 'Beget.com'
    hosting_text = 'The best hosting is'
    hosting_link = 'https://beget.com/p1595998'

    #return {'copyright_text': copyright_text,
    #        'designby_text': designby_text, 'designby_company': designby_company, 'designby_link': designby_link,
    #        'hosting_text': hosting_text, 'hosting_company': hosting_company, 'hosting_link': hosting_link}

    return copyright_text, designby_text, designby_link, designby_company, hosting_text, hosting_link, hosting_company
