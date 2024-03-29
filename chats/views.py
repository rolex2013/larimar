# import datetime
from datetime import datetime, timedelta
from django.utils import timezone

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# from datetime import datetime, date, time
from django.db.models import Q, Count, Min, Max, Sum, Avg

from django.views.generic import CreateView

from companies.models import Company  # , UserCompanyComponentGroup
from .models import Dict_ChatType, Chat, Message, ChatMember
from main.models import Component
from companies.models import UserCompanyComponentGroup
from django.contrib.auth.models import User

# from .forms import ChatForm, MessageForm

from django.db.models import Q

from django.utils.translation import gettext_lazy as _
"""
path('chats_list/<int:companyid>/', views.chats, name='chats'),
path('chats_page/chat_create/<int:companyid>/', views.ChatCreate.as_view(), name='chat_create'),
path('chats_page/message_list/<int:chatid>', views.messages, name='messages'),
path('chats_page/message_create/<int:chatid>', views.MessageCreate.as_view(), name='message_create'),
"""


def chats_messages_members_lists(request, companyid=0, chatid=0):
    if companyid == 0:
        companyid = request.session["_auth_user_currentcompany_id"]
    current_company = (Company.objects.filter(id=companyid).select_related(
        "currency", "structure_type", "type", "author").first())

    comps = request.session["_auth_user_companies_id"]
    currentuser = request.user.id

    chats_list = Chat.objects.filter(
        Q(author=currentuser)
        | Q(members__in=[
            currentuser,
        ])
        | Q(type=3),
        company_id=companyid,
        is_active=True,
    ).select_related("company", "author", "type")

    if chatid == 0:
        # messages_list = []
        # members_list = []
        currentchat = None
        # template_name = "company_detail.html"
    else:
        # messages_list = Message.objects.filter(chat_id=chatid, is_active=True, chat__members__in=[currentuser,]).select_related("chat", "author") #.prefetch_related("chat__members")
        currentchat = Chat.objects.filter(
            id=chatid).first()  # messages_list[0].chat

        # members_list = ChatMember.objects.filter(chat=currentchat, is_active=True, dateclose__isnull=True).select_related("member", "author")

    chat_type_list = Dict_ChatType.objects.filter(is_active=True)

    button_company_select = _("Сменить организацию")

    return {
        "nodes_chats": chats_list.distinct(),
        # 'nodes_messages': messages_list,
        # 'nodes_members': members_list,
        "component_name": "chats",
        "current_company": current_company,
        "companyid": current_company.id,
        "currentchat": currentchat,
        "currentchatid": 0,
        # 'chats_list_reload': 0,
        "user_companies": comps,
        "chat_type_list": chat_type_list,
        "button_company_select": button_company_select,
    }


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def chats(request, companyid=0, chatid=0):
    request.session["_auth_user_currentcomponent"] = "chats"
    request.session["_auth_user_currentcomponentid"] = (
        Component.objects.filter(code="chats", is_active=True).first().id)
    # print('=====================', Component.objects.filter(Q(code='chats') & Q(is_active=True)))

    render_list = chats_messages_members_lists(request, companyid, chatid)

    # template_name = 'chats_list.html'
    template_name = "company_detail.html"
    # template_name = "chats.html"
    # print(render_list)
    # print("websocket_test:", request.session['websocket_test'])

    return render(request, template_name, render_list)


# class ChatCreate(CreateView):
#    #model = Chat
#    #form_class = ChatForm
#    #template_name = 'object_form.html'
#    pass


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def chatcreate(request, **kwargs):
    get = kwargs.pop("get", {})
    # Если чат создаётся командой из другого чата
    if get:
        companyid = get["companyid"]
        name = get["name"]
        description = get["description"]
        type = get["typeid"]
    else:
        companyid = request.GET["companyid"]
        name = request.GET["name"]
        description = request.GET["description"]
        type = request.GET["typeid"]
    currentuserid = request.user.id

    # print(companyid)
    chat_new = Chat.objects.create(
        company_id=companyid,
        name=name,
        description=description,
        type_id=type,
        author_id=currentuserid,
    )
    if chat_new:
        member_new = ChatMember.objects.create(
            chat_id=chat_new.id,
            is_admin=True,
            author_id=currentuserid,
            member_id=currentuserid,
        )
    render_list = chats_messages_members_lists(request, companyid=0, chatid=0)
    # chats_list = Chat.objects.filter(Q(author=currentuserid) | Q(members__in=[currentuserid,]) | Q(type=3), company_id=companyid, is_active=True).select_related("company", "author", "type")
    # chat_type_list = Dict_ChatType.objects.filter(is_active=True)

    return render(request, "chats_list.html", render_list,
                  {"currentchatid": chat_new.id})
    # return render(request, 'chats_list.html', {'nodes_chats': chats_list.distinct(),
    #                                           'companyid': companyid,
    #                                           'chat_type_list': chat_type_list,
    #                                           }, {'object_message': 'Ok!'})


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def messages(request):
    chatid = request.GET["chatid"]
    interval = request.GET["interval"]
    currentuserid = request.user.id

    ChatMember.objects.filter(chat_id=chatid,
                              member_id=request.user.id).update(
                                  dateonline=datetime.now(),
                                  datecurrent=datetime.now())
    currentchat = Chat.objects.filter(
        id=chatid).select_related("company").first()

    mess_list = Message.objects.filter(
        Q(onlyfor__isnull=True)
        | Q(onlyfor=currentuserid)
        | Q(chat__author_id=currentuserid),
        chat_id=chatid,
        is_active=True,
    ).distinct()

    if interval == "1":
        template_name = "chat_messages_list.html"
    else:
        template_name = "chat_messages_members.html"

    # ChatMember.objects.filter(chat_id=chatid, member_id=request.user.id).update(dateonline=datetime.now())

    # print(chatid, interval, currentuserid, template_name)

    return render(
        request,
        template_name,
        {
            "nodes_messages":
            mess_list,
            "nodes_members":
            ChatMember.objects.filter(
                chat=chatid,
                is_active=True, dateclose__isnull=True).select_related(
                    "member", "author").order_by("-is_admin", "-dateonline"),
            "currentchat":
            currentchat,
            "currentchatid":
            chatid,
            "companyid":
            currentchat.company_id,
            # 'chats_list_reload': 0,
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def messagecreate(request):
    chatid = request.GET["chatid"]
    text = request.GET["text"]
    currentuserid = request.user.id
    # для команды добавления участников чата
    currentcompanyid = request.session["_auth_user_currentcompany_id"]
    currentcomponentid = request.session["_auth_user_currentcomponentid"]
    # print(currentcompanyid, currentcomponentid)

    message_new = Message.objects.create(chat_id=chatid,
                                         text=text,
                                         author_id=currentuserid)
    if message_new:
        pass

    template = "chat_messages_members.html"
    text = text.strip()
    # *** Обрабатываем команды ***
    chats_list_reload = 0
    if text[0] == "/":
        member = ChatMember.objects.filter(chat_id=chatid,
                                           member_id=currentuserid,
                                           is_active=True).first()
        if member.is_admin:
            # print(text[0:5], text.find('/help'))
            # if text.find('/help') >= 0:
            if text[0:5] == "/help":
                text_new = (
                    '/chat-create [-t 1|2|3] -n[ame] "название чата" [-d[escription] "описание чата"]<br />'
                    '/chat-update [-t 1|2|3] [-n[ame] "название чата"] [-d[escription] "описание чата"]<br />'
                    '<span style="padding:0px 0px 0px 16px;">/name "название чата"</span><br />'
                    '<span style="padding:0px 0px 0px 16px;">/description "описание чата"</span><br />'
                    "/user-invite [-u[ser]] username [-a[dmin]]<br />"
                    '<span style="padding:0px 0px 0px 16px;">/invite [-u[ser]] username [-a[dmin]]</span><br />'
                    "/user-update [-u[ser]] username [-a[dmin]]<br />"
                    '<span style="padding:0px 0px 0px 16px;">/admin [-u[ser]] username [-a[dmin]]</span><br />'
                    "/user-kick [-u[ser]] username [[-t[ime]] часов]<br />"
                    '<span style="padding:0px 0px 0px 16px;">/kick [-u[ser]] username [[-t[ime]] часов]</span>"'
                )
            else:
                # print(text[0:12])
                if text[0:12] == "/chat-create":
                    # op_t_1 = text.find('-t')
                    # op_t_2 = text.find('-topic')
                    chat_new = Chat()
                    if text.find("-name") >= 0 or text.find("-n") >= 0:
                        # txt = text.split('"')[1].split('"')[0]
                        # print(txt)
                        chat_new.name = text.split('"')[1]
                    if text.find("-description") >= 0 or text.find("-d") >= 0:
                        com_cnt = text.count('"')
                        if com_cnt == 2:
                            chat_new.description = text.split('"')[1]
                        elif com_cnt == 4:
                            chat_new.description = text.split('"')[3]
                    # print(text.split(' ')[0], text.split(' ')[1], text.split(' ')[2], text.split(' ')[3])
                    if text.find("-type") >= 0 or text.find("-t") >= 0:
                        chat_new.type_id = text.split(" ")[2]
                    else:
                        chat_new.type_id = 3
                    if chat_new.name or chat_new.description:
                        chat_new.company_id = message_new.chat.company_id
                        chat_new.author_id = currentuserid
                        chat_new.save()
                        member_new = ChatMember.objects.create(
                            chat_id=chatid,
                            member_id=currentuserid,
                            is_admin=True,
                            author_id=currentuserid,
                        )
                        chatid = chat_new.id
                        text_new = _("Создан новый чат") + \
                            " " + chat_new.name + '"'
                        chats_list_reload = 1

                elif text[0:12] == "/chat-update":
                    # text_new = "Вы ввели команду: /chat-update"
                    chat_curr = Chat.objects.filter(id=chatid).first()
                    # print(com_count, chat_curr)
                    if text.find("-name") >= 0 or text.find("-n") >= 0:
                        chat_curr.name = text.split('"')[1]
                    if text.find("-description") >= 0 or text.find("-d") >= 0:
                        com_cnt = text.count('"')
                        if com_cnt == 2:
                            chat_curr.description = text.split('"')[1]
                        elif com_cnt == 4:
                            chat_curr.description = text.split('"')[3]
                    if text.find("-type") >= 0 or text.find("-t") >= 0:
                        chat_curr.type_id = text.split(" ")[2]
                    chat_curr.save()
                    # print(chat_curr)
                    text_new = _("Текущий чат изменён!")
                    chats_list_reload = 1
                    # template = 'company_detail.html'
                    # template = 'chats.html'
                # elif:
                else:
                    text_new = _("Такой команды не существует!")

        else:
            text_new = _(
                "Сожалеем, но у Вас нет прав Администратора для выполнения команд в этом чате!"
            )

        message_new.onlyfor_id = currentuserid
        message_new.save()
        command_new = Message.objects.create(
            chat_id=chatid,
            text=text_new,
            onlyfor_id=currentuserid,
            author_id=currentuserid,
        )

    # *** Конец обработки команд *************************

    messages_list = Message.objects.filter(
        Q(onlyfor__isnull=True)
        | Q(onlyfor=currentuserid)
        | Q(chat__author_id=currentuserid),
        chat_id=chatid,
        is_active=True,
        chat__members__in=[
            currentuserid,
        ],
    ).select_related("chat", "author")  # .prefetch_related("chat__members")
    # messages_list = Message.objects.filter(chat_id=chatid, is_active=True).distinct()

    # Message.objects.filter(exec(text))
    # print(Message.objects.filter(exec(text)))

    currentchat = Chat.objects.filter(id=chatid).first()
    # print(currentchat, chatid)
    # print(messages_list)

    return render(
        request,
        template,
        {
            "nodes_messages":
            messages_list.distinct(),
            "nodes_members":
            ChatMember.objects.filter(
                chat=chatid,
                is_active=True, dateclose__isnull=True).select_related(
                    "member", "author").order_by("-is_admin", "-dateonline"),
            "currentchat":
            currentchat,
            "currentchatid":
            chatid,
            "chats_list_reload":
            chats_list_reload,
            "object_message":
            "Ok!",
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def messageform(request):
    chatid = request.GET["chatid"]

    currentchat = Chat.objects.filter(id=chatid).first()

    return render(
        request,
        "chat_message_form.html",
        {
            "currentchat": currentchat,
            "currentchatid": chatid,
            "chats_list_reload": 0,
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def membercreate(request):
    chatid = request.GET["chatid"]
    memberid = request.GET["memberid"]
    memberisadmin = request.GET["memberisadmin"]

    isadmin = False
    if memberisadmin == "1":
        isadmin = True

    # currentchat = Chat.objects.filter(id=chatid).first()
    currentuserid = request.user.id

    member_new = ChatMember.objects.create(chat_id=chatid,
                                           member_id=memberid,
                                           is_admin=isadmin,
                                           author_id=currentuserid)

    (member_list, currentchat) = memberlist(request, chatid)

    return render(
        request,
        "chat_messages_members.html",
        {
            "nodes_messages":
            Message.objects.filter(chat_id=chatid, is_active=True).distinct(),
            "nodes_members":
            ChatMember.objects.filter(
                chat=chatid,
                is_active=True, dateclose__isnull=True).select_related(
                    "member", "author").order_by("-is_admin", "-dateonline"),
            "currentchat":
            currentchat,
            "currentchatid":
            chatid,
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def memberform(request):
    chatid = request.GET["chatid"]

    (member_list, currentchat) = memberlist(request, chatid)

    return render(
        request,
        "chat_member_form.html",
        {
            "currentchat": currentchat,
            "currentchatid": chatid,
            "member_list": member_list,
        },
    )


def memberlist(request, chatid):
    currentchat = Chat.objects.filter(id=chatid).first()

    member_list = []

    is_admin = ChatMember.objects.filter(chat_id=chatid,
                                         member_id=request.user.id).first()
    # print(chatid, request.user.id, 'is_admin=', is_admin)
    if is_admin:
        # Список пользователей для выбора
        # uc = UserCompanyComponentGroup.objects.filter(company_id=currentchat.company_id, component__name="Чаты", is_active=True).select_related(
        # "user", "component").distinct() #.values_list('user_id', flat=True)
        # print(Component.objects)
        uc = (UserCompanyComponentGroup.objects.filter(
            company_id=currentchat.company_id,
            component__code="chats",
            is_active=True,
        ).select_related("user", "component").distinct())
        # print(uc)
        current_members_list = ChatMember.objects.filter(
            chat_id=chatid, is_active=True).values_list("member_id", flat=True)
        # member_list = User.objects.filter(~Q(id__in=current_members_list), id__in=uc, is_active=True) #.exclude(id__in=current_members_list)
        # member_list = User.objects.filter(id__in=uc, is_active=True).exclude(id__in=current_members_list)
        # mem_list = uc.exclude(user_id__in=current_members_list)
        # print(current_members_list)
        for mem in uc:
            # print('+++', mem.user_id, mem.company_id, mem.component_id,
            #       mem.group_id)
            if mem.user_id not in current_members_list:
                member_list.append(mem)
            # else:
            #     print('---', mem, mem.user_id, current_members_list)
            #     pass
                # print(mem)
        # print('===', uc)
        # print(current_members_list)
        # print(member_list)

    return (member_list, currentchat)


def ajax_memberlist(request):
    chatid = request.GET["chatid"]
    currentchat = Chat.objects.filter(id=chatid).first()

    return render(
        request,
        "chat_members_list.html",
        {
            "currentchat":
            currentchat,
            "currentchatid":
            chatid,
            "nodes_members":
            ChatMember.objects.filter(
                chat=chatid,
                is_active=True, dateclose__isnull=True).select_related(
                    "member", "author").order_by("-is_admin", "-dateonline"),
        },
    )


def chatslist(request):
    companyid = request.GET["companyid"]
    currentuser = request.user.id

    chats_list = Chat.objects.filter(
        Q(author=currentuser)
        | Q(members__in=[
            currentuser,
        ])
        | Q(type=3),
        company_id=companyid,
        is_active=True,
    )  # .select_related("company", "author", "type")

    # print('===', chats_list.distinct())

    return render(
        request,
        "chats_list.html",
        {
            "nodes_chats": chats_list.distinct(),
            # 'chats_list_reload': 0,
        },
    )


def get_current_company_id(request):
    print(request)

    return request.session["_auth_user_currentcompany_id"]


# ***
# def wschat(request):
#
#    user_list = User.objects.filter(is_active=True)
#
#    return render(request, 'chat_ws.html', {'user_list': user_list,})
