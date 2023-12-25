# import os
# import socket
# import redis

from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseRedirect

from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView

from accounts.models import UserProfile
from main.models import Notification, Meta_ObjectType, ModelLog
from projects.models import Project, Task, ProjectFile  # , TaskFile
from crm.models import Client, ClientTask, ClientEvent, ClientFile
from docs.models import Doc, DocTask, DocVerFile
from files.models import Folder, FolderFile
from django.contrib.auth.models import User

from django.db.models import Q  # , Count, Min, Max, Sum, Avg

from django.contrib.auth.decorators import login_required

import json

# from django.utils import translation


def websocket_test(request):
    ok = request.GET["ok"]
    # r = redis.Redis(host="127.0.0.1", port="6379")
    # try:
    #    is_connected = r.ping()
    # except redis.ConnectionError:
    #    print('Redis connect error!')
    request.session["websocket_test"] = ok
    print("WebSocket:", ok)
    # return render(request, "sidebar.html", {'wstest': ok,})
    return render(
        request,
        "main_wstest.html",
        {
            "wstest": ok,
        },
    )


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена!</h1>")


# def accessDenided(request, exception):
#    return HttpResponseNotFound('<h1>Доступ запрещён!</h1>')


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
class ProjectsHome(TemplateView):
    template_name = "main.html"


# class Home(ListView):


def notificationread(request):
    # меняем статус прочитанности уведомления

    notify_id = request.GET["val"]
    status_selectid = int(request.GET["st"])
    notificationobjecttype = request.GET["ot"]
    notify = Notification.objects.get(id=notify_id)
    # print(notify_id, status_selectid, notificationobjecttype)
    # curr_notify = (
    #     Notification.objects.filter(id=notify_id)
    #     .select_related("author", "recipient", "objecttype", "type")
    #     .first()
    # )
    curr_notify = Notification.objects.filter(id=notify_id).select_related(
        "author", "recipient", "objecttype", "type").first()
    # print('notify', notify.datecreate, notify.text)
    # print('curr_notify', curr_notify.datecreate, curr_notify.text)
    if curr_notify:
        # print('**************************',
        #       curr_notify.author, curr_notify.is_read_isauthor)
        if curr_notify.author.id == request.user.id:

            if curr_notify.is_read_isauthor:
                notify.is_read_isauthor = False
            else:
                notify.is_read_isauthor = True
            notify.save(update_fields=["is_read_isauthor"])
        else:
            if curr_notify.is_read_isrecipient:
                notify.is_read_isrecipient = False
            else:
                notify.is_read_isrecipient = True
            notify.save(update_fields=["is_read_isrecipient"])

    if status_selectid == 2:
        notification_list = Notification.objects.filter(
            Q(author=request.user.id, is_read_isauthor=False)
            | Q(recipient=request.user.id, is_read_isrecipient=False),
            is_active=True,
            # is_read=False,
            type_id=3)
    elif status_selectid == 3:
        notification_list = Notification.objects.filter(
            # Q(recipient_id=request.user.id) | Q(author_id=request.user.id),
            Q(author=request.user.id, is_read_isauthor=True)
            | Q(recipient=request.user.id, is_read_isrecipient=True),
            is_active=True,
            # is_read=True,
            type_id=3)
    else:
        notification_list = Notification.objects.filter(
            Q(recipient_id=request.user.id) | Q(author_id=request.user.id),
            is_active=True,
            type_id=3)
    if notificationobjecttype != "0":
        notification_list = notification_list.filter(
            objecttype_id=notificationobjecttype)

    metaobjecttype_list = Meta_ObjectType.objects.filter(is_active=True)

    return render(
        request,
        "notify_list.html",
        {
            "notification_list":
            notification_list.select_related(
                "author", "recipient", "objecttype",
                "type").distinct().order_by("-datecreate"),
            "metaobjecttype_list":
            metaobjecttype_list.distinct().order_by(),
            "status_selectid":
            status_selectid,
            "metaobjecttype_selectid":
            notificationobjecttype,
            # 'qq':
            # (curr_notify.id, status_selectid),
        },
    )


def notificationlist(userid, notificationstatus, notificationobjecttype):
    notification_list = Notification.objects.filter(
        Q(recipient_id=userid) | Q(author_id=userid),
        is_active=True,
        type_id=3)
    # print('===', notificationobjecttype, notification_list)
    if notificationstatus == "2":
        notification_list = notification_list.filter(Q(author=userid, is_read_isauthor=False) |
                                                     Q(recipient=userid, is_read_isrecipient=False))
    elif notificationstatus == "3":
        # notification_list = notification_list.filter(is_read=True)
        notification_list = notification_list.filter(Q(author=userid, is_read_isauthor=True) |
                                                     Q(recipient=userid, is_read_isrecipient=True))
    notification_list = notification_list.select_related(
        "author", "recipient", "objecttype", "type")
    # print('==============', notification_list)

    if notificationobjecttype != "0":
        notification_list = notification_list.filter(
            objecttype_id=notificationobjecttype)
        # print(notificationobjecttype, notification_list)

    return notification_list


def notificationfilter(request):
    # currentuser = request.user.id
    notificationstatus = request.GET["notificationstatus"]
    notificationobjecttype = request.GET["notificationobjecttype"]

    # notification_list = Notification.objects.filter(
    #     Q(recipient_id=request.user.id) | Q(author_id=request.user.id),
    #     is_active=True,
    #     type_id=3)
    # # print('===', notificationobjecttype, notification_list)
    # if notificationstatus == "2":
    #     notification_list = notification_list.filter(is_read=False)
    # elif notificationstatus == "3":
    #     notification_list = notification_list.filter(is_read=True)
    # notification_list = notification_list.select_related(
    #     "author", "recipient", "objecttype", "type"
    # )
    # # print(notification_list)

    # if notificationobjecttype != "0":
    #     notification_list = notification_list.filter(
    #         objecttype_id=notificationobjecttype
    #     )
    #     # print(notificationobjecttype, notification_list)

    notification_list = notificationlist(request.user.id, notificationstatus,
                                         notificationobjecttype)

    metaobjecttype_list = Meta_ObjectType.objects.filter(is_active=True)

    return render(
        request,
        "notify_list.html",
        {
            "notification_list": notification_list.distinct().order_by("-datecreate"),
            "metaobjecttype_list": metaobjecttype_list.distinct().order_by(),
            "status_selectid": notificationstatus,
            "metaobjecttype_selectid": notificationobjecttype,
        },
    )


def sidebarnotificationfilter(request):
    # notificationuser = request.user.id
    # # notificationuser = request.GET['notificationuser']
    notificationstatus = request.GET["notificationstatus"]
    notificationobjecttype = request.GET["notificationobjecttype"]

    # notification_list = Notification.objects.filter(
    #     Q(recipient_id=notificationuser) | Q(author_id=notificationuser),
    #     is_active=True,
    #     type_id=3,
    # )
    # # print('===', notificationuser, notificationobjecttype)
    # if notificationstatus == "2":
    #     notification_list = notification_list.filter(is_read=False)
    # elif notificationstatus == "3":
    #     notification_list = notification_list.filter(is_read=True)
    #     # print(str(notification_list))

    # if notificationobjecttype != "0":
    #     notification_list = notification_list.filter(
    #         objecttype_id=notificationobjecttype
    #     )

    # cnt = notification_list.filter(
    #     recipient_id=request.user.id, is_read=False, objecttype_id=9
    # ).count()
    # # print(cnt)
    # notification_list = (
    #     notification_list.select_related("author", "recipient", "objecttype", "type")
    #     .order_by("datecreate")
    #     .distinct()
    # )
    # # print(notification_list)
    notification_list = notificationlist(request.user.id, notificationstatus,
                                         notificationobjecttype)
    count_unread = notification_list.filter(
        Q(author=request.user.id, is_read_isauthor=False) |
        Q(recipient=request.user.id, is_read_isrecipient=False)).count()

    return render(
        request,
        "sidebar_notifications_list.html",
        {
            "nodes": notification_list,
            "currentuserid": request.user.id,
            "count_unread": count_unread,
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def objecthistory(request, objtype="prj", pk=0):
    if objtype == "prj":
        if pk == 0:
            current_object = 0
        else:
            current_object = (
                Project.objects.filter(id=pk)
                .select_related(
                    "company",
                    "author",
                    "assigner",
                    "status",
                    "type",
                    "structure_type",
                    "currency",
                )
                .first()
            )
        templatename = "project_history.html"
    elif objtype == "tsk":
        if pk == 0:
            current_object = 0
        else:
            current_object = (
                Task.objects.filter(id=pk)
                .select_related(
                    "project", "author", "assigner", "status", "type", "structure_type"
                )
                .first()
            )
        templatename = "task_history.html"
    elif objtype == "clnt":
        if pk == 0:
            current_object = 0
        else:
            current_object = (
                Client.objects.filter(id=pk)
                .select_related(
                    "company",
                    "author",
                    "user",
                    "initiator",
                    "manager",
                    "status",
                    "type",
                    "protocol_type",
                    "currency",
                )
                .first()
            )
        templatename = "client_history.html"
    elif objtype == "cltsk":
        if pk == 0:
            current_object = 0
        else:
            current_object = (
                ClientTask.objects.filter(id=pk)
                .select_related(
                    "assigner",
                    "author",
                    "client",
                    "status",
                    "structure_type",
                    "type",
                    "initiator",
                )
                .first()
            )
        templatename = "clienttask_history.html"
    elif objtype == "clevnt":
        if pk == 0:
            current_object = 0
        else:
            current_object = (
                ClientEvent.objects.filter(id=pk)
                .select_related(
                    "assigner",
                    "author",
                    "client",
                    "status",
                    "task",
                    "type",
                    "initiator",
                )
                .first()
            )
        templatename = "clientevent_history.html"
    elif objtype == "doc":
        if pk == 0:
            current_object = 0
        else:
            current_object = (
                Doc.objects.filter(id=pk)
                .select_related("company", "author", "status", "type", "manager")
                .first()
            )
        templatename = "doc_history.html"
    elif objtype == "dctsk":
        if pk == 0:
            current_object = 0
        else:
            current_object = (
                DocTask.objects.filter(id=pk)
                .select_related("assigner", "author", "doc", "docver", "status", "type")
                .first()
            )
        templatename = "doctask_history.html"

    comps = request.session["_auth_user_companies_id"]

    # формируем массив заголовков
    # row = ModelLog.objects.filter(modelobjectid=pk, is_active=True).first()
    # row = ModelLog.objects.get(modelobjectid=pk, is_active=True)
    # titles = json.loads(row.log).items()
    # print(objtype)
    nodes = ModelLog.objects.filter(
        componentname=objtype, modelobjectid=pk, is_active=True
    ).select_related(
        "author"
    )  # , "modelobject") #.order_by()
    # print(nodes)
    i = -1
    mas = []
    for node in nodes:
        i += 1
        mas.append(json.loads(node.log).items())
        # print(mas[i])

    return render(
        request,
        templatename,
        {
            # 'titles': titles,
            "nodes": nodes,
            "mas": mas,
            "current_object": current_object,
            "user_companies": comps,
            "objtype": objtype,
            # 'table': table,
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def objectfiledelete(request, objtype="prj"):
    fileid = request.GET["fileid"]
    # print(fileid)
    # print(objtype)
    obj_files_rights = request.GET["obj_files_rights"]
    object_message = ""
    template = "objectfile_list.html"
    if fileid:
        if objtype[:3] == "prj":
            fl = ProjectFile.objects.filter(id=fileid).first()
        elif objtype[:3] == "cln":
            fl = ClientFile.objects.filter(id=fileid).first()
        elif objtype[:3] == "doc":
            fl = DocVerFile.objects.filter(id=fileid).first()
        elif objtype[:3] == "fld":
            fl = FolderFile.objects.filter(id=fileid).first()
        if fl.is_active == True:
            fl.is_active = False
        else:
            fl.is_active = True
        fl.save(update_fields=["is_active"])
    if objtype == "prj":
        files = ProjectFile.objects.filter(
            project_id=fl.project_id, is_active=True
        ).order_by("uname")
    elif objtype == "prjtsk":
        files = ProjectFile.objects.filter(task_id=fl.task_id, is_active=True).order_by(
            "uname"
        )
    elif objtype == "prjtskcmnt":
        files = ProjectFile.objects.filter(
            taskcomment_id=fl.taskcomment_id, is_active=True
        ).order_by("uname")
    elif objtype == "clnt":
        files = ClientFile.objects.filter(
            client_id=fl.client_id, is_active=True
        ).order_by("uname")
    elif objtype == "clnttsk":
        files = ClientFile.objects.filter(task_id=fl.task_id, is_active=True).order_by(
            "uname"
        )
    elif objtype == "clnttskcmnt":
        files = ClientFile.objects.filter(
            taskcomment_id=fl.taskcomment_id, is_active=True
        ).order_by("uname")
    elif objtype == "clntevnt":
        files = ClientFile.objects.filter(
            event_id=fl.event_id, is_active=True
        ).order_by("uname")
    elif objtype == "clntevntcmnt":
        files = ClientFile.objects.filter(
            teventcomment_id=fl.eventcomment_id, is_active=True
        ).order_by("uname")
    elif objtype == "doc":
        files = DocVerFile.objects.filter(
            docver_id=fl.docver_id, is_active=True
        ).order_by("uname")
    elif objtype == "doctsk":
        files = DocVerFile.objects.filter(task_id=fl.task_id, is_active=True).order_by(
            "uname"
        )
    elif objtype == "doctskcmnt":
        files = DocVerFile.objects.filter(
            taskcomment_id=fl.taskcomment_id, is_active=True
        ).order_by("uname")
    elif objtype == "fldr":
        files = FolderFile.objects.filter(
            folder_id=fl.folder_id, is_active=True
        )  # .order_by('uname')
        template = "folderfile_list.html"
    return render(
        request,
        template,
        {
            "objtype": objtype,
            "files": files,
            "obj_files_rights": obj_files_rights,
            "object_message": object_message,
            "media_path": settings.MEDIA_URL,
        },
    )


# ***
def notifications(request):
    user_list = User.objects.filter(is_active=True)
    # return render(request, 'sidebar_notifications~.html', {'recipientusernameid': '10',
    #                                              }
    #              )

    return render(
        request,
        "sidebar.html",
        {
            "user_list": user_list,
        },
    )


def sidebarnotificationisread(request):
    userid = request.GET["userid"]

    # Notification.objects.filter(
    #     recipient_id=userid, type_id=3, objecttype_id=9, is_read=False
    # ).update(is_read=True)
    Notification.objects.filter(Q(recipient_id=userid) | Q(author_id=userid),
                                type_id=3,
                                is_read_isrecipient=False).update(is_read_isrecipient=True)
    # print('recipient_id=',userid, 'type_id=',3, 'objecttype_id=',9, 'is_read=',False)
    notification_list = Notification.objects.filter(
        # Q(recipient_id=userid) | Q(author_id=userid),
        Q(author=userid, is_read_isauthor=False) |
        Q(recipient=userid, is_read_isrecipient=False),
        is_active=True,
        # is_read=False,
        type_id=3,
    )
    # cnt = notification_list.exclude(author_id=request.user.id, objecttype_id=9).count()
    # cnt = notification_list.filter(
    #     recipient_id=userid, is_read=False, objecttype_id=9
    # ).count()
    # cnt = notification_list.filter(recipient_id=userid, is_read=False).count()
    # print(cnt)
    # metaobjecttype_list = Meta_ObjectType.objects.filter(is_active=True).order_by("sort").distinct()
    notification_list = (
        notification_list.select_related("author", "recipient", "objecttype")
        .order_by("datecreate")
        .distinct()
    )
    count_unread = notification_list.filter(Q(author=userid, is_read_isauthor=False) |
                                            Q(recipient=userid, is_read_isrecipient=False)).count()

    return render(
        request,
        "sidebar_notifications_list.html",
        {
            "nodes": notification_list,
            "status_selectid": "2",
            # 'metaobjecttype_list': metaobjecttype_list,
            "currentuserid": request.user.id,
            "count_unread": count_unread,
        },
    )


# def select_lang(request):
#     lang_code = request.GET['lang_code']
#     go_next = request.META.get('HTTP_REFERER', '/')
#     response = HttpResponseRedirect(go_next)
#     #print('code=', lang_code, 'go_next=', go_next)
#     if lang_code and translation.check_for_language(lang_code):
#         if hasattr(request, 'session'):
#             request.session['django_language'] = lang_code
#             request.session['_language'] = lang_code
#         else:
#             response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
#         translation.activate(lang_code)
#     return response
#     #return render(request, 'base.html') #response


def select_lang(request):
    lang_code = request.GET["lang_code"]
    # print('=== select_lang ===')
    response = HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    if lang_code:
        request.session[settings.LANGUAGE_SESSION_KEY] = lang_code
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
        # print("***", lang_code, "***", settings.LANGUAGE_COOKIE_NAME)
        if request.user.is_authenticated:
            UserProfile.objects.filter(user_id=request.user.id).update(lang=lang_code)
    else:
        if request.user.is_authenticated:
            user_lang = (
                UserProfile.objects.filter(user_id=request.user.id).first().lang.strip()
            )
            if user_lang is not None and user_lang != "":
                request.session[settings.LANGUAGE_SESSION_KEY] = user_lang
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_lang)
            # else:
            #    request.session[settings.LANGUAGE_SESSION_KEY] = user_lang
            #    request.session['_auth_user_currentlang_id'] = settings.LANGUAGE_COOKIE_NAME
        else:
            request.session[
                settings.LANGUAGE_SESSION_KEY
            ] = settings.LANGUAGE_COOKIE_NAME
    # print('code=', lang_code, 'response=', request.META.get('HTTP_REFERER', '/'))

    return response
