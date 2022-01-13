from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView

from companies.models import Company #, UserCompanyComponentGroup
from .models import Dict_ChatType, Chat, Message

#from .forms import ChatForm, MessageForm

"""
path('chats_list/<int:companyid>/', views.chats, name='chats'),
path('chats_page/chat_create/<int:companyid>/', views.ChatCreate.as_view(), name='chat_create'),
path('chats_page/message_list/<int:chatid>', views.messages, name='messages'),
path('chats_page/message_create/<int:chatid>', views.MessageCreate.as_view(), name='message_create'),
"""

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def chats(request, companyid=0):

    if companyid == 0:
        companyid = request.session['_auth_user_currentcompany_id']
    current_company = Company.objects.filter(id=companyid).first()
    #print(current_company)
    comps = request.session['_auth_user_companies_id']

    chat_list = Chat.objects.filter(company_id=companyid, is_active=True)
    #template_name = 'chats_list.html'
    template_name = "company_detail.html"
    return render(request, template_name, {
                                            'nodes_chats': chat_list,
                                            'component_name': 'chats',
                                            'current_company': current_company,
                                            'companyid': current_company.id,
                                            'user_companies': comps,
                                          }
                  )

class ChatCreate(CreateView):
    #model = Chat
    #form_class = ChatForm
    #template_name = 'object_form.html'
    pass


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def messages(request, chatid=None):
    message_list = Message.objects.filter(chat_id=chatid, is_active=True)
    template_name = 'messages_list.html'
    return render(request, template_name, {
                                            'nodes_messages': message_list,
                                          }
                  )

class MessageCreate(CreateView):
    # model = Message
    # form_class = MessageForm
    # template_name = 'object_form.html'
    pass
