
#import datetime
from datetime import datetime, timedelta
from django.utils import timezone

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#from datetime import datetime, date, time
from django.db.models import Q, Count, Min, Max, Sum, Avg

from django.views.generic import CreateView

from companies.models import Company #, UserCompanyComponentGroup
from .models import Dict_ChatType, Chat, Message, ChatMember
from companies.models import UserCompanyComponentGroup
from django.contrib.auth.models import User

#from .forms import ChatForm, MessageForm

from django.db.models import Q

"""
path('chats_list/<int:companyid>/', views.chats, name='chats'),
path('chats_page/chat_create/<int:companyid>/', views.ChatCreate.as_view(), name='chat_create'),
path('chats_page/message_list/<int:chatid>', views.messages, name='messages'),
path('chats_page/message_create/<int:chatid>', views.MessageCreate.as_view(), name='message_create'),
"""

def chats_messages_members_lists(request, companyid=0, chatid=0):

    if companyid == 0:
        companyid = request.session['_auth_user_currentcompany_id']
    current_company = Company.objects.filter(id=companyid).select_related("currency", "structure_type", "type", "author").first()

    comps = request.session['_auth_user_companies_id']
    currentuser = request.user.id

    chats_list = Chat.objects.filter(Q(author=currentuser) | Q(members__in=[currentuser,]) | Q(type=3), company_id=companyid, is_active=True).select_related("company", "author", "type")

    if chatid == 0:
        messages_list = []
        members_list = []
        currentchat = None
        template_name = "company_detail.html"
    else:
        #messages_list = Message.objects.filter(chat_id=chatid, is_active=True, chat__members__in=[currentuser,]).select_related("chat", "author") #.prefetch_related("chat__members")
        currentchat = Chat.objects.filter(id=chatid).first() #messages_list[0].chat

        #members_list = ChatMember.objects.filter(chat=currentchat, is_active=True, dateclose__isnull=True).select_related("member", "author")

    chat_type_list = Dict_ChatType.objects.filter(is_active=True)

    button_company_select = "Сменить организацию"

    return {
            'nodes_chats': chats_list.distinct(),
            #'nodes_messages': messages_list,
            #'nodes_members': members_list,
            'component_name': 'chats',
            'current_company': current_company,
            'companyid': current_company.id,
            'currentchat': currentchat,
            'currentchatid': 0,
            'user_companies': comps,
            'chat_type_list': chat_type_list,
            'button_company_select': button_company_select,
           }

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def chats(request, companyid=0, chatid=0):

    render_list = chats_messages_members_lists(request, companyid, chatid)

    #template_name = 'chats_list.html'
    template_name = "company_detail.html"
    #print(render_list)

    return render(request, template_name, render_list)

#class ChatCreate(CreateView):
#    #model = Chat
#    #form_class = ChatForm
#    #template_name = 'object_form.html'
#    pass

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def chatcreate(request):
    companyid = request.GET['companyid']
    name = request.GET['name']
    description = request.GET['description']
    type = request.GET['typeid']
    currentuserid = request.user.id
    #print(companyid)
    chat_new = Chat.objects.create(company_id=companyid, name=name, description=description, type_id=type, author_id=currentuserid)
    if chat_new:
        member_new = ChatMember.objects.create(chat_id=chat_new.id, is_admin=True, author_id=currentuserid, member_id=currentuserid)
    render_list = chats_messages_members_lists(request, companyid=0, chatid=0)
    #chats_list = Chat.objects.filter(Q(author=currentuserid) | Q(members__in=[currentuserid,]) | Q(type=3), company_id=companyid, is_active=True).select_related("company", "author", "type")
    #chat_type_list = Dict_ChatType.objects.filter(is_active=True)

    return render(request, 'chats_list.html', render_list, {'object_message': 'Ok!'})
    #return render(request, 'chats_list.html', {'nodes_chats': chats_list.distinct(),
    #                                           'companyid': companyid,
    #                                           'chat_type_list': chat_type_list,
    #                                           }, {'object_message': 'Ok!'})

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def messages(request):

    chatid = request.GET['chatid']
    interval = request.GET['interval']

    if interval == 1:
        template_name = 'chat_messages_list.html'
    else:
        template_name = 'chat_messages_members.html'

    ChatMember.objects.filter(chat_id=chatid, member_id=request.user.id).update(dateonline=datetime.now())

    return render(request, template_name, {
                                            'nodes_messages': Message.objects.filter(chat_id=chatid, is_active=True).distinct(),
                                            'nodes_members': ChatMember.objects.filter(chat=chatid, is_active=True, dateclose__isnull=True).select_related("member", "author").order_by('-is_admin', '-dateonline'),
                                            'currentchat': Chat.objects.filter(id=chatid).first(),
                                            'currentchatid': chatid,
                                          }
                  )

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def messagecreate(request):

    chatid = request.GET['chatid']
    text = request.GET['text']
    currentuserid = request.user.id

    message_new = Message.objects.create(chat_id=chatid, text=text, author_id=currentuserid)
    if message_new:
        pass

    messages_list = Message.objects.filter(chat_id=chatid, is_active=True,
                                           chat__members__in=[currentuserid, ]).select_related("chat",
                                                                                               "author")  # .prefetch_related("chat__members")
    #messages_list = Message.objects.filter(chat_id=chatid, is_active=True).distinct()

    currentchat = Chat.objects.filter(id=chatid).first()
    #print(currentchat, chatid)
    #print(messages_list)

    return render(request, 'chat_messages_members.html', {'nodes_messages': messages_list.distinct(),
                                                          'nodes_members': ChatMember.objects.filter(chat=chatid,
                                                                                                     is_active=True,
                                                                                                     dateclose__isnull=True).select_related("member", "author").order_by('-is_admin', '-dateonline'),
                                                          'currentchat': currentchat,
                                                          'currentchatid': chatid,
                                                          'object_message': 'Ok!'
                                                          #'chat_type_list': chat_type_list,
                                                         },

                  )

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def messageform(request):

    chatid = request.GET['chatid']

    currentchat = Chat.objects.filter(id=chatid).first()

    return render(request, 'chat_message_form.html', {'currentchat': currentchat, 'currentchatid': chatid,})

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def membercreate(request):

    chatid = request.GET['chatid']
    memberid = request.GET['memberid']
    memberisadmin = request.GET['memberisadmin']

    isadmin = False
    if memberisadmin == "1":
        isadmin = True

    currentchat = Chat.objects.filter(id=chatid).first()
    currentuserid = request.user.id

    member_new = ChatMember.objects.create(chat_id=chatid, member_id=memberid, is_admin=isadmin, author_id=currentuserid)


    return render(request, 'chat_messages_members.html', {'nodes_messages': Message.objects.filter(chat_id=chatid, is_active=True).distinct(),
                                                          'nodes_members': ChatMember.objects.filter(chat=chatid,
                                                                                                     is_active=True,
                                                                                                     dateclose__isnull=True).select_related("member", "author").order_by('-is_admin', '-dateonline'),
                                                          'currentchat': currentchat,
                                                          'currentchatid': chatid,
                                                          },
                  )

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def memberform(request):

    chatid = request.GET['chatid']

    currentchat = Chat.objects.filter(id=chatid).first()

    # Список пользователей для выбора
    uc = UserCompanyComponentGroup.objects.filter(company_id=currentchat.company_id).distinct().values_list('user_id', flat=True)
    current_members_list = ChatMember.objects.filter(chat_id=chatid, is_active=True).values_list('member_id', flat=True)
    #member_list = User.objects.filter(~Q(id__in=current_members_list), id__in=uc, is_active=True) #.exclude(id__in=current_members_list)
    member_list = User.objects.filter(id__in=uc, is_active=True).exclude(id__in=current_members_list)
    print(uc)
    print(current_members_list)
    print(member_list)

    return render(request, 'chat_member_form.html', {'currentchat': currentchat, 'currentchatid': chatid, 'member_list': member_list,})


