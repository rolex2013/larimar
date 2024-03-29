from django.conf import settings
from django.shortcuts import render
import json, requests
import os  # для записи путей к файлам

import random, string

from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date, time
from django.db.models import Q, Count, Min, Max, Sum, Avg


from .serializers import (
    Dict_SystemSerializer,
    CompanySerializer,
)  # , FeedbackTicketSerializer, FeedbackTicketCommentSerializer
from companies.models import Company, UserCompanyComponentGroup
from .models import (
    Dict_System,
    Dict_FeedbackTicketStatus,
    Dict_FeedbackTicketType,
    Dict_FeedbackTaskStatus,
)
from .models import (
    FeedbackTicket,
    FeedbackTicketComment,
    FeedbackTask,
    FeedbackTaskComment,
    FeedbackFile,
)
from .forms import (
    Dict_SystemForm,
    FeedbackTicketForm,
    FeedbackTaskForm,
    FeedbackTicketCommentForm,
    FeedbackTaskCommentForm,
)

from main.utils import AddFilesMixin

from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    Dict_SystemSerializer,
    FeedbackTicketSerializer,
    FeedbackTicketCommentSerializer,
    FeedbackFileSerializer,
)

# from django.core.serializers.json import DjangoJSONEncoder
# from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO  # , StringIO
import base64
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, requires_csrf_token, csrf_exempt
from django.utils.translation import gettext_lazy as _


def get_client_ip(request):
    """Getting client Ip"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def generate_alphanum_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = "".join(random.sample(letters_and_digits, length))
    # print("Alphanum Random string of length", length, "is:", rand_string)
    return rand_string


# *** API техподдержки ***

# decorators = [csrf_exempt, requires_csrf_token]
decorators = [csrf_exempt]


@method_decorator(decorators, name="create")
class Dict_SystemViewSet(viewsets.ModelViewSet):
    queryset = Dict_System.objects.all()  # .order_by('name')
    serializer_class = Dict_SystemSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def get_serializer_context(self):
    #    """
    #    Extra context provided to the serializer class.
    #    """
    #    return {
    #        'request': self.request,
    #        'format': self.format_kwarg,
    #        'view': self
    #    }

    # @csrf_exempt
    def create(self, request):
        sys_data = request.data
        new_sys = Dict_System.objects.create(
            code=sys_data["code"],
            name=sys_data["name"],
            domain=sys_data["domain"],
            url=sys_data["url"],
            ip=sys_data["ip"],
            email=sys_data["email"],
            phone=sys_data["phone"],
            is_local=sys_data["is_local"],
        )
        # new_sys.save()
        # serializer = Dict_SystemSerializer(new_sys, context={'request': request})
        sys_local = Dict_System.objects.filter(is_local=True, is_active=True).first()
        if sys_data["req"] == True:
            # *** Добавление системы разработчика в удалённую БД ***
            """
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            #ip = get_client_ip(self.request)
            #url = self.request.build_absolute_uri('/')[:-1]
            system_data = {'code': sys_local.code, 'name': sys_local.name, 'domain': sys_local.domain, 'url': sys_local.url,
                           'ip': sys_local.ip, 'email': sys_local.email, 'phone': sys_local.phone, 'is_local': False, 'req': False}
            url = sys_data["url"] + '/feedback/api/system/'
            #url = 'http://larimaritgroup.ru/feedback/api/system/'
            r = requests.post(url, headers=headers, data=json.dumps(system_data))
            upd_sys = Dict_System.objects.filter(id=new_sys.id)
            upd_sys.requeststatuscode = r.status_code
            upd_sys.save()
            """
            # sys = Dict_System.objects.filter(code="1YES-1YES-1YES-1YES", is_local=True, is_active=True).first()
            serializer = Dict_SystemSerializer(sys_local, context={"request": request})
        return Response(serializer.data)

    # def update(self, request, pk=None):
    #    return Response(serializer.data)


# ""
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()  # .order_by('name')
    serializer_class = CompanySerializer


# ""


class FeedbackTicketViewSet(viewsets.ModelViewSet):
    queryset = FeedbackTicket.objects.filter(is_active=True).order_by("-datecreate")
    serializer_class = FeedbackTicketSerializer
    # permission_classes = (IsAuthenticated,)
    filter_fields = ("name", "description", "is_active", "status", "type")
    """
    #def get(self, request):
    def list(self, request):
        tickets = FeedbackTicket.objects.all()
        serializer = FeedbackTicketSerializer(tickets, many=True)
        return Response({"tickets": serializer.data})
    #def post(self, request):
    def create(self, request):
        ticket = request.data.get("ticket")
        # Create an ticket from the above data
        serializer = FeedbackTicketSerializer(data=ticket)
        if serializer.is_valid(raise_exception=True):
            ticket_saved = serializer.save()
        return Response({"success": "Ticket '{}' created successfully".format(ticket_saved.title)})
    #def put(self, request, pk):
    def retrieve(self, request, pk):
        saved_ticket = get_object_or_404(FeedbackTicket.objects.all(), pk=pk)
        data = request.data.get('ticket')
        serializer = FeedbackTicketSerializer(instance=saved_ticket, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            ticket_saved = serializer.save()
        return Response({
            "success": "Ticket '{}' updated successfully".format(ticket_saved.title)
        })
    """

    def create(self, request):
        ticket_data = request.data

        try:
            systemcode = ticket_data["systemcode"]
            try:
                # sys = Dict_System.objects.filter(is_local=True, is_active=True).first()
                sys = Dict_System.objects.filter(
                    code=systemcode, is_active=True
                ).first()
                systemid = sys.id
            except:
                systemid = 1
                text = (
                    _("Система с кодом")
                    + " {} ".format(systemcode)
                    + _("не зарегистрирована!")
                )
                response_data = {"text": text}
                return Response(response_data)
        except:
            sys = Dict_System.objects.filter(is_local=True, is_active=True).first()
            systemid = sys.id

        try:
            type = Dict_FeedbackTicketType.objects.filter(
                name=ticket_data["type"]
            ).first()
            typeid = type.id
        except:
            typeid = 1

        try:
            status = Dict_FeedbackTicketStatus.objects.filter(
                name=ticket_data["status"]
            ).first()
            statusid = status.id
        except:
            statusid = 1

        try:
            idremote = int(ticket_data["id_remote"])
            new_ticket = FeedbackTicket.objects.create(
                name=ticket_data["name"],
                description=ticket_data["description"],
                system_id=systemid,
                status_id=statusid,
                type_id=typeid,
                id_remote=idremote,
            )
            # new_ticket.save()
            # new_ticket = FeedbackTicket.objects.filter(id=3).first()
        except:
            new_ticket = FeedbackTicket(
                name=ticket_data["name"],
                description=ticket_data["description"],
                system_id=systemid,
                status_id=statusid,
                type_id=typeid,
            )

        serializer = FeedbackTicketSerializer(new_ticket, context={"request": request})

        return Response(serializer.data)

    def put(self, request):
        data = request.data
        pk = data["id"]
        sys = Dict_System.objects.filter(
            code=data["systemcode"], is_active=True
        ).first()
        data["system_id"] = sys.id
        saved_ticket = FeedbackTicket.objects.filter(pk=pk).first()
        serializer = FeedbackTicketSerializer(
            instance=saved_ticket, data=data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            ticket_saved = serializer.save()
            status = Dict_FeedbackTicketStatus.objects.filter(
                name=data["status"]
            ).first()
            type = Dict_FeedbackTicketType.objects.filter(name=data["type"]).first()
            saved_ticket = FeedbackTicket.objects.filter(pk=pk).update(
                status=status.id, type=type.id
            )
        return Response(
            {
                "success": _("Тикет")
                + " {} ".format(str(ticket_saved.id) + ". " + ticket_saved.name)
                + _("успешно изменён!")
            }
        )


class FeedbackTicketCommentViewSet(viewsets.ModelViewSet):
    queryset = FeedbackTicketComment.objects.filter(is_active=True).order_by(
        "-datecreate"
    )
    serializer_class = FeedbackTicketCommentSerializer
    filter_fields = (
        "name",
        "description",
    )

    def create(self, request):
        comment_data = request.data
        systemcode = comment_data["systemcode"]
        ticketremoteid = int(comment_data["ticketid"])
        commentdescription = comment_data["description"]
        commentname = comment_data["name"]
        idremote = int(comment_data["id_remote"])

        try:
            # ticket = FeedbackTicket.objects.filter(ticket_id=ticketid).first()
            # print(systemcode)
            sys = Dict_System.objects.filter(code=systemcode, is_active=True).first()
            systemid = sys.id
            try:
                ticket = FeedbackTicket.objects.filter(
                    system_id=systemid, id_remote=ticketremoteid
                ).first()
                ticketid = ticket.id
                # new_ticketcomment = FeedbackTicketComment.objects.create(ticket_id=ticketid, name=commentname, description=commentdescription)
                new_ticketcomment = FeedbackTicketComment.objects.create(
                    ticket_id=ticketid,
                    name=commentname,
                    description=commentdescription,
                    id_remote=idremote,
                    is_active=True,
                )
                serializer = FeedbackTicketCommentSerializer(
                    new_ticketcomment, context={"request": request}
                )
                return Response(serializer.data)
            except:
                # тут надо сообщить отправителю, что такого тикета у разработчика нет!
                text = _("Нет такого тикета!")
                response_data = {"text": text}
                return Response(response_data)
        except:
            text = (
                _("Система с кодом")
                + " '"
                + systemcode
                + "' "
                + _("не зарегистрирована!")
            )
            response_data = {"text": text}
            return Response(response_data)

        # new_ticketcomment = FeedbackTicketComment.objects.create(ticket_id=ticketid, name=commentname, description=commentdescription)
        # try:
        #    idremote = int(comment_data["id_remote"])
        new_ticketcomment = FeedbackTicketComment.objects.create(
            ticket_id=ticketid,
            name=commentname,
            description=commentdescription,
            id_remote=idremote,
            is_active=True,
        )
        # except:
        #    new_ticketcomment = FeedbackTicketComment.objects.create(ticket_id=ticketid, name=commentname,
        #                                                             description=commentdescription,
        #                                                             is_active=True)
        serializer = FeedbackTicketCommentSerializer(
            new_ticketcomment, context={"request": request}
        )
        return Response(serializer.data)


# def FeedbackTicketCreateAPI(request):
#    return


def add_files(request, files, ticketid, commentid=None):
    for f in files:
        # print('===', f)
        fcnt = FeedbackFile.objects.filter(name=f, is_active=True).count()
        fl = FeedbackFile(ticket_id=ticketid, ticketcomment_id=commentid, pfile=f)
        # fl.author = self.request.user
        fn = f
        if fcnt:
            f_str = str(f)
            ext_pos = f_str.rfind(".")
            fn = f_str[0:ext_pos] + " (" + str(fcnt) + ")" + f_str[ext_pos : len(f_str)]
        fl.name = f
        fl.uname = fn
        fl.save()
        fullpath = os.path.join(settings.MEDIA_ROOT, str(fl.pfile))
        fl.psize = os.path.getsize(fullpath)
        # print('+++', fl)
        fl.save()
    return FeedbackFileSerializer(fl, context={"request": request})


class FeedbackFileViewSet(viewsets.ModelViewSet):
    queryset = FeedbackFile.objects.all()
    serializer_class = FeedbackFileSerializer
    # filter_fields = ('name', 'description',)
    filter_fields = ("name", "ticket")

    def create(self, request):
        # *** добавление файлов ***
        files = request.data.getlist("feedbackticket_file")
        # print(files)

        try:
            ticketremoteid = int(request.data["ticketid"])
            try:
                ticket = FeedbackTicket.objects.filter(id_remote=ticketremoteid).first()
                ticketid = ticket.id
            except:
                return Response(
                    {
                        "files": _("Тикет")
                        + " id_remote="
                        + str(ticketremoteid)
                        + " "
                        + _("не найден!")
                    }
                )

            try:
                ticketcommentremoteid = int(request.data["ticketcommentid"])
                try:
                    ticketcomment = FeedbackTicketComment.objects.filter(
                        id_remote=ticketcommentremoteid
                    ).first()
                    ticketcommentid = ticketcomment.id
                except:
                    return Response(
                        {
                            "files": _("Комментарий")
                            + " id_remote="
                            + str(ticketcommentremoteid)
                            + " "
                            + _("тикета")
                            + " id_remote="
                            + str(ticketremoteid)
                            + " "
                            + _("не найден!")
                        }
                    )
            except:
                ticketcommentid = None
        except:
            return Response({"files": _("Не передан id Тикета!")})

        serializer = add_files(request, files, ticketid, ticketcommentid)
        return Response({"files": serializer.data})

    def list(self, request):
        files = FeedbackFile.objects.filter(is_active=True)
        serializer = FeedbackFileSerializer(
            files, context={"request": request}, many=True
        )
        return Response({"files": serializer.data})


# ******


class Dict_SystemCreate(CreateView):
    model = Dict_System
    form_class = Dict_SystemForm
    # template_name = 'feedbackticket_create.html'
    template_name = "object_form.html"

    # def get_success_url(self):
    #    print(self.object) # Prints the name of the submitted user
    #    print(self.object.id) # Prints None
    #    return reverse("webApp:feedbackticket:stepTwo", args=(self.object.id,))

    def form_valid(self, form):
        # self.object = form.save() # Созадём новую Систему
        # *** Добавление системы в удалённую БД ***
        ip = get_client_ip(self.request)
        url = self.request.build_absolute_uri("/")[:-1]
        # print(self.request.build_absolute_uri('/')[:-1])
        # генерация уникального кода для регистрируемой Системы
        code = (
            generate_alphanum_random_string(4)
            + "-"
            + generate_alphanum_random_string(4)
            + "-"
            + generate_alphanum_random_string(4)
            + "-"
            + generate_alphanum_random_string(4)
        )
        # print('ip=', ip, '   code=', code)
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        # system_data = {'name': self.object.name, 'domain': self.object.domain, 'url': self.object.url, 'ip': self.object.ip, 'email': self.object.email, 'phone': self.object.phone}
        # system_data = {'code': code, 'name': self.object.name, 'domain': self.object.domain, 'url': self.object.url, 'ip': ip,
        #               'email': self.object.email, 'phone': self.object.phone}
        # system_data = {'code': code, 'name': form.cleaned_data["name"], 'domain': form.cleaned_data["domain"], 'url': form.cleaned_data["url"],
        #               'ip': ip, 'email': form.cleaned_data["email"], 'phone': form.cleaned_data["phone"]}
        system_data = {
            "code": code,
            "name": form.cleaned_data["name"],
            "domain": form.cleaned_data["domain"],
            "url": url,
            "ip": ip,
            "email": form.cleaned_data["email"],
            "phone": form.cleaned_data["phone"],
            "is_local": False,
            "req": True,
        }
        url_dev = "http://larimaritgroup.ru/feedback/api/system/"
        # url = 'http://localhost:8000/feedback/api/system/'
        try:
            r = requests.post(url_dev, headers=headers, data=json.dumps(system_data))
            # r = requests.post(url, headers=headers, csrfmiddlewaretoken=csrftoken, data=json.dumps(system_data))
            form.instance.code = code
            form.instance.ip = ip
            form.instance.url = url
            form.instance.requeststatuscode = r.status_code
            self.object = form.save()  # Создаём новую Систему
            rj = r.json()
            # print(rj)
            # print(rj.get("code"), rj.get("name"), rj.get("domain"), rj.get("url"), rj.get("ip"), rj.get("email"), rj.get("phone"), rj.get("is_local"))
            sys_dev = Dict_System.objects.create(
                code=rj.get("code"),
                name=rj.get("name"),
                domain=rj.get("domain"),
                url=rj.get("url"),
                ip=rj.get("ip"),
                email=rj.get("email"),
                phone=rj.get("phone"),
                is_local=False,
                requeststatuscode=200,
            )
        except:
            print(_("Что-то пошло не так с сервером..."))
        # ***
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Регистрация новой Системы")
        return context

    # def get_form_kwargs(self):
    #    kwargs = super().get_form_kwargs()
    #    is_support_member = self.request.session['_auth_user_issupportmember']
    #    # здесь нужно условие для 'action': 'create'
    #    kwargs.update({'action': 'create', 'name': self.kwargs['systemid'], 'companyid': self.kwargs['companyid'], 'is_support_member': is_support_member})
    #    return kwargs


def definerights(request, companyid):
    if companyid is None:
        return (True, True, True, True, False)

    currentuser = request.user.id
    currentusercompanyid = request.session["_auth_user_currentcompany_id"]
    is_support_member = False
    is_support_admin_org = False
    is_superadmin = False
    is_admin_org = False
    is_admin = False

    current_company = Company.objects.filter(id=companyid).first()

    if current_company.is_support is True:
        # Является ли юзер сотрудником этой Службы поддержки?
        if companyid in request.session["_auth_user_companies_id"]:
            is_support_member = True
        # Является ли юзер Администратором этой Службы поддержки?
        try:
            UserCompanyComponentGroup.objects.filter(
                user_id=currentuser, company_id=companyid, group_id=2
            )
            is_support_admin_org = True
        except:
            is_support_admin_org = False
    # Является ли юзер Администратором своей организации?
    try:
        UserCompanyComponentGroup.objects.filter(
            user_id=currentuser, company_id=currentusercompanyid, group_id=2
        )
        is_admin_org = True
        is_admin = True
    except:
        is_admin_org = False
        is_admin = False
    # Является ли юзер Суперадмином?
    if 1 in request.session["_auth_user_group_id"]:
        # print(usergroupid)
        is_superadmin = True
        is_admin = True
    return (
        is_support_member,
        is_support_admin_org,
        is_admin_org,
        is_admin,
        is_superadmin,
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def feedbacktickets(request, is_ticketslist_dev=0, systemid=1, companyid=0):
    # def feedbacktickets(request, companyid=0):

    currentuser = request.user.id
    currentusercompanyid = request.session["_auth_user_currentcompany_id"]

    try:
        systemdev = Dict_System.objects.filter(
            is_active=True, code="1YES-1YES-1YES-1YES"
        ).first()
    except:
        systemdev = ""

    systemdevid = request.session["system_dev"][0]
    is_system_dev = request.session["system_dev"][1]

    # feedbackticket_list = FeedbackTicket.objects.filter(is_active=True)  # .select_related("status", "type", "company", "companyfrom", "system", "author")
    feedbackticket_list = FeedbackTicket.objects.filter(is_active=True).select_related(
        "status", "type", "company", "companyfrom", "system", "author"
    )
    # print("+++++++++++++", feedbackticket_list)

    if companyid == 0:
        # Проверяем наличие хоть одной Службы поддержки в Системе
        support_list = Company.objects.filter(is_active=True, is_support=True)
        support_count = len(support_list)
        if support_count == 0:
            # В системе нет ни одной Службы техподдержки!
            return render(request, "companies.html", {"len_list": 0})
        elif support_count == 1:
            # В системе только одна Служба техподдержки
            companyid = support_list[0].id
        else:
            # В системе несколько Служб техподдержки.
            try:
                # Пробуем выбрать по последнему отправленному тикету
                mylastticket = feedbackticket_list.filter(
                    author_id=currentuser, company_id__isnull=False
                ).order_by("-id")[0]
                companyid = mylastticket.company_id
            except:
                # если тикет не найден, то выбираем первую Службу техподдержки
                companyid = support_list[0].id

    current_company = (
        Company.objects.filter(id=companyid)
        .select_related("currency", "structure_type", "type", "author")
        .first()
    )
    # print(current_company)
    request.session["_auth_user_currentcomponent"] = "feedback"

    # Видимость пункта "- Все" в фильтрах
    (
        is_support_member,
        is_support_admin_org,
        is_admin_org,
        is_admin,
        is_superadmin,
    ) = definerights(request, companyid)

    # request.session['_auth_user_issupportmember'] = is_support_member
    request.session["_auth_user_supportcompany_id"] = companyid

    if is_ticketslist_dev == 1:
        # список тикетов разработчику
        if is_system_dev:
            # список тикетов разработчику в системе разработчика 1YES!
            # feedbackticket_list = feedbackticket_list.filter(system_id=systemdevid)
            feedbackticket_list = feedbackticket_list.exclude(system_id=systemdevid)
            # print(systemdevid, feedbackticket_list)
        else:
            # список тикетов разработчику в локальной системе
            feedbackticket_list = feedbackticket_list.filter(
                system_id=systemdevid, company_id__isnull=True, companyfrom_id=companyid
            )
        template_name = "feedbacksystemdev_detail.html"
    else:
        # список тикетов внутри системы
        template_name = "company_detail.html"
        feedbackticket_list = feedbackticket_list.exclude(system=systemdevid)
        # tktstatus = "0"
        # *** фильтруем по статусу и принадлежности ***
        try:
            tktstatus = request.POST["select_feedbackticketstatus"]
        except:
            if is_support_member:
                feedbackticket_list = feedbackticket_list.filter(
                    company=companyid, dateclose__isnull=True
                )
            else:
                feedbackticket_list = feedbackticket_list.filter(
                    Q(author=request.user.id), company=companyid, dateclose__isnull=True
                )
        else:
            if tktstatus == "0":
                # если в выпадающем списке выбрано "Все активные"
                feedbackticket_list = feedbackticket_list.filter(
                    Q(author=request.user.id), company=companyid, dateclose__isnull=True
                )
            else:
                # Суперадмин видит все тикеты всех организаций этой Службы поддержки
                feedbackticket_list = feedbackticket_list.filter(
                    Q(author=request.user.id), company=companyid
                )
                if tktstatus == "-1":
                    # если в выпадающем списке выбрано "Все"
                    if is_admin_org:
                        # Админ Организации видит все тикеты своей организации этой Службы поддержки
                        feedbackticket_list = feedbackticket_list.filter(
                            companyfrom=currentusercompanyid
                        )
                elif tktstatus == "-2":
                    # если в выпадающем списке выбрано "Просроченные"
                    feedbackticket_list = feedbackticket_list.filter(
                        dateclose__isnull=True, dateend__lt=datetime.now()
                    )
                else:
                    feedbackticket_list = feedbackticket_list.filter(status=tktstatus)
            # print('-----------------------', tktstatus)
        # *******************************

    button_feedbackticketdev = ""
    button_feedbackticketdev_create = ""
    # len_task_list = 0
    if is_support_member is True:
        # feedbackticket_task_list = FeedbackTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id), ticket__company=companyid,
        #                                                dateclose__isnull=True) #.exclude(ticket__system=systemdevid)
        # feedbackticket_task_list = tickettasklist(request, companyid, "-1", "-1", "-1", is_ticketslist_dev)
        # len_task_list = len(feedbackticket_task_list)
        button_feedbackticketdev = _("Обращения к разработчику")
        button_feedbackticketdev_create = _("Добавить")

    # len_list = len(feedbackticket_list)

    comps = request.session["_auth_user_companies_id"]

    # Заполняем списки справочников для фильтров
    ticketstatus = Dict_FeedbackTicketStatus.objects.filter(is_active=True)
    tickettype = Dict_FeedbackTicketType.objects.filter(is_active=True)

    comps_support = Company.objects.filter(is_active=True, is_support=True)
    if len(comps_support) < 2:
        button_company_select = ""
    else:
        button_company_select = _("Сменить службу техподдержки")
    button_feedbackticket_create = _("Добавить")
    # Проверяем кол-во компаний - служб техподдержки
    is_many_support_member = True
    is_support_member = False
    if len(request.session["_auth_user_compsupportid"]) > 0:
        is_support_member = True
    len_task_list = 0

    tskstatus_selectid = "0"  # - Все активные задачи
    tskstatus_myselectid = "3"  # - Все мои задачи
    if is_support_member:
        # сотрудникам Техподдержки показывать только те компании, где они работают
        comps_support = Company.objects.filter(
            is_active=True, is_support=True, id__in=comps
        )
        if len(comps_support) == 1:
            # если пользователь является сотрудником только одной Техподдержки, то он не может выбрать другую службу
            is_many_support_member = False
            # button_company_select = ''
        task_list = tickettasklist(
            request,
            companyid,
            "0",
            tskstatus_selectid,
            tskstatus_myselectid,
            is_ticketslist_dev,
        )
        # len_task_list = len(task_list)
        task_list_distinct = task_list.distinct()
        len_task_list = len(task_list_distinct)
    else:
        task_list_distinct = None
        len_task_list = 0

    # tktstatus = "0"
    # print("==================", tktstatus, feedbackticket_list.distinct())

    # Добавляем Систему в справочник
    is_system_reged = True
    dsys_cnt = Dict_System.objects.filter(is_active=True).count()
    if dsys_cnt == 0:
        is_system_reged = False

    current_companyid = request.session["_auth_user_supportcompany_id"]

    # if is_system_dev:
    #    template_name = "feedbacksystemdev_detail.html"
    # else:
    #    template_name = "company_detail.html"

    return render(
        request,
        template_name,
        {
            "nodes_tickets": feedbackticket_list.distinct(),  # .order_by(), # для удаления задвоений и восстановления иерархии
            "nodes": task_list_distinct,  # order_by(),
            "component_name": "feedback",
            "current_company": current_company,
            "current_companyid": current_companyid,
            "current_ticketid": 0,
            "is_system_dev": is_system_dev,
            "is_ticketslist_dev": is_ticketslist_dev,
            "systemdev": systemdev,
            "systemdevid": systemdevid,
            "companyid": companyid,
            "user_companies": comps,
            "button_company_select": button_company_select,
            "is_system_reged": is_system_reged,
            "button_feedbackticketdev": button_feedbackticketdev,
            "button_feedbackticket_create": button_feedbackticket_create,
            "button_feedbackticketdev_create": button_feedbackticketdev_create,
            "feedbackticketstatus": ticketstatus,
            "feedbackticketstatus_selectid": "0",
            "feedbacktickettype": tickettype,
            "feedbacktickettype_selectid": "-1",
            "myfeedbackticket_myselectid": "1",
            "tskstatus_selectid": tskstatus_selectid,
            "tskstatus_myselectid": tskstatus_myselectid,
            "object_list": "feedbacktask_list",
            "taskstatus": Dict_FeedbackTaskStatus.objects.filter(is_active=True),
            # "len_list": len_list,
            "len_task_list": len_task_list,
            "is_support_member": is_support_member,
            "is_admin": is_admin,
            "is_admin_org": is_admin_org,
            "is_many_support_member": is_many_support_member,
        },
    )


class FeedbackTicketDetail(DetailView):
    model = FeedbackTicket
    template_name = "feedbackticket_detail.html"


# class MyJsonEncoder(DjangoJSONEncoder):
#    def default(self, o):
#        if isinstance(o, InMemoryUploadedFile):
#           return o.read()
#        return str(o)


class FeedbackTicketCreate(AddFilesMixin, CreateView):
    model = FeedbackTicket
    form_class = FeedbackTicketForm
    # template_name = 'feedbackticket_create.html'
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.system_id = self.kwargs["systemid"]
        sys = Dict_System.objects.filter(
            is_active=True, id=form.instance.system_id
        ).first()
        sysloc = Dict_System.objects.filter(is_active=True, is_local=True).first()
        compid = self.kwargs["companyid"]
        if compid != 0 and sys.is_local:  # is True # == True
            form.instance.company_id = compid
            form.instance.companyfrom_id = self.request.session[
                "_auth_user_currentcompany_id"
            ]
        else:
            # в тикет разработчику пишем id текущей службы техподдержки
            form.instance.companyfrom_id = compid
        form.instance.author_id = self.request.user.id
        form.instance.companyfrom_id = self.request.session[
            "_auth_user_currentcompany_id"
        ]
        # form.instance.status_id = 1 # Новому Тикету присваиваем статус "Новый"
        # form.instance.system_id = 1  # Новый Тикет временно приписываем к локальной Системе
        print('*******', sys.is_local, form.instance.author_id, form.instance.id)
        self.object = form.save()  # Созадём новый тикет
        af = self.add_files(
            form, "feedback", "ticket"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        # отправляем тикет разработчику
        if not sys.is_local:  # == False:
            headers = {"Content-type": "application/json", "Accept": "application/json"}
            ticket_data = {
                "name": form.instance.name,
                "description": form.instance.description,
                "status": str(form.instance.status),
                "type": str(form.instance.type),
                "id_remote": str(self.object.id),
                "systemcode": sysloc.code,
            }
            url_dev = sys.url + "/feedback/api/ticket/"
            r = requests.post(url_dev, headers=headers, data=json.dumps(ticket_data))
            if af and r.status_code < 300:
                # *** отправляем вдогонку файлы ***
                files = FeedbackFile.objects.filter(ticket_id=self.object.id).prefetch
                fl = []
                for f in files:
                    fl.append(
                        (
                            "feedbackticket_file",
                            (
                                str(f.name),
                                open(settings.MEDIA_ROOT + "/" + str(f.pfile), "rb"),
                            ),
                        )
                    )
                url_dev = sys.url + "/feedback/api/file/"
                r_f = requests.request(
                    "POST",
                    url_dev,
                    headers={},
                    data={"ticketid": str(self.object.id)},
                    files=fl,
                )

            # тикету для разработчика прописываем id текущей компании техподдержки
            self.object.companyfrom_id = compid
            # print(r, r.content, r.json()["id"])
            self.object.id_remote = r.json()["id"]
            self.object.requeststatuscode = r.status_code
            self.object = form.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Новый Тикет")
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # is_support_member = self.request.session['_auth_user_issupportmember']
        is_support_member = False
        if len(self.request.session["_auth_user_compsupportid"]) > 0:
            is_support_member = True
        # здесь нужно условие для 'action': 'create'
        # print(self.kwargs['systemid'])
        kwargs.update(
            {
                "user": self.request.user,
                "action": "create",
                "systemid": self.kwargs["systemid"],
                "companyid": self.kwargs["companyid"],
                "is_support_member": is_support_member,
                "is_system_dev": self.request.session["system_dev"][1],
            }
        )
        return kwargs


class FeedbackTicketUpdate(AddFilesMixin, UpdateView):
    model = FeedbackTicket
    form_class = FeedbackTicketForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        # context = super(ProjectUpdate, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context["header"] = "Изменить Тикет"
        # kwargs = super(ProjectUpdate, self).get_form_kwargs()
        kwargs = super().get_form_kwargs()
        context["files"] = FeedbackFile.objects.filter(
            ticket_id=self.kwargs["pk"], is_active=True
        ).order_by("uname")
        # print(context)
        # print(kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # is_support_member = self.request.session['_auth_user_issupportmember']
        is_support_member = False
        if len(self.request.session["_auth_user_compsupportid"]) > 0:
            is_support_member = True
        # здесь нужно условие для 'action': 'update'
        kwargs.update(
            {
                "user": self.request.user,
                "action": "update",
                "is_support_member": is_support_member,
                "is_system_dev": self.request.session["system_dev"][1],
            }
        )
        return kwargs

    def form_valid(self, form):
        sys = Dict_System.objects.filter(
            is_active=True, id=form.instance.system_id
        ).first()
        sysloc = Dict_System.objects.filter(is_active=True, is_local=True).first()
        self.object = form.save(
            commit=False
        )  # без commit=False происходит вызов save() Модели
        af = self.add_files(
            form, "feedback", "ticket"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        comment = form.cleaned_data["comment"]
        self.object = form.save()
        # *** отправляем изменения тикета разработчику ***
        if sys.is_local == False:
            headers = {"Content-type": "application/json", "Accept": "application/json"}
            ticket_data = {
                "id": self.object.id_remote,
                "name": self.object.name,
                "description": self.object.description,
                "status": str(self.object.status),
                "type": str(self.object.type),
                "id_remote": str(self.object.id),
                "systemcode": sysloc.code,
            }
            url_dev = sys.url + "/feedback/api/ticket/"
            # print(sys.url, ticket_data)
            r = requests.put(url_dev, headers=headers, data=json.dumps(ticket_data))
            # print(r.status_code, r.json())
            """
            if af and r.status_code < 300:
                # *** отправляем вдогонку файлы ***
                files = form.files.getlist('files')
                print(form.files, '/', form.files.getlist('files'), '/')
                #files = FeedbackFile.objects.filter(ticket_id=self.object.id)
                fl = []
                for f in files:
                    fl.append(('feedbackticket_file', (str(f.name), open(settings.MEDIA_ROOT+'/'+str(f), 'rb'))))
                    #print(fl)
                url_dev = sys.url + '/feedback/api/file/'
                r_f = requests.request("POST", url_dev, headers={}, data={'ticketid': str(self.object.id)}, files=fl)
                #print(r_f.text)
            """
            self.object.requeststatuscode = r.status_code
            self.object = form.save()
        # *** ***
        if comment != "":
            # создаём Комментарий к Тикету
            company_id = self.request.session["_auth_user_supportcompany_id"]
            cmnt = FeedbackTicketComment.objects.create(
                ticket_id=self.object.id,
                company_id=company_id,
                author_id=self.object.author_id,
                description=comment,
            )

            if sys.is_local == False:
                # отправляем коммент разработчику
                # print(sysloc)
                headers = {
                    "Content-type": "application/json",
                    "Accept": "application/json",
                }
                ticket_data = {
                    "name": cmnt.name,
                    "description": cmnt.description,
                    "systemcode": sysloc.code,
                    "ticketid": str(cmnt.ticket_id),
                    "id_remote": str(cmnt.id),
                }
                url_dev = cmnt.ticket.system.url + "/feedback/api/ticketcomment/"
                r = requests.post(
                    url_dev, headers=headers, data=json.dumps(ticket_data)
                )
                # print(r)
                # self.object.requeststatuscode = r.status_code
                # self.object = form.save()
                # cmnt = FeedbackTicketComment(id=cmnt.id)
                cmnt.id_remote = r.json()["id"]
                cmnt.requeststatuscode = r.status_code
                cmnt.save()

        return super().form_valid(form)


# *** FeedbackTask ***
@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def feedbacktasks(request, is_ticketslist_dev=0, ticketid=0, pk=0):
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    # currentusercompanyid = request.session['_auth_user_currentcompany_id']
    # print(currentusercompanyid)
    tskstatus_selectid = 0

    currentticket = (
        FeedbackTicket.objects.filter(id=ticketid)
        .select_related("system", "company", "companyfrom", "author", "type", "status")
        .first()
    )

    # показываем только "Мои задачи"
    tskstatus_myselectid = "3"
    task_list = tickettasklist(
        request,
        currentticket.company_id,
        ticketid,
        "0",
        tskstatus_myselectid,
        is_ticketslist_dev,
    )
    # len_list = len(task_list)

    ticketcomment_list = FeedbackTicketComment.objects.filter(
        ticket_id=ticketid, is_active=True
    ).select_related(
        "ticket", "company", "author", "ticket__company", "ticket__company__currency"
    )

    ticketcomment_costsum = currentticket.costcommentsum
    task_costsum = currentticket.costtasksum
    taskcomment_costsum = currentticket.costtaskcommentsum
    taskcomment_timesum = currentticket.timesum
    try:
        sec = taskcomment_timesum["time__sum"] * 3600
    except:
        sec = 0
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    seconds = sec

    # права на удаление файлов
    obj_files_rights = 0

    if pk == 0:
        current_task = 0
        root_task_id = 0
        tree_task_id = 0
        if currentuser == currentticket.author_id:
            obj_files_rights = 1
    else:
        current_task = (
            FeedbackTask.objects.filter(id=pk)
            .select_related(
                "ticket",
                "ticket__company",
                "ticket__company__currency",
                "author",
                "status",
                "assigner",
            )
            .first()
        )
        root_task_id = current_task.get_root().id
        tree_task_id = current_task.tree_id
        if (
            currentuser == current_task.author_id
            or currentuser == current_task.assigner_id
        ):
            obj_files_rights = 1

    (
        is_support_member,
        is_support_admin_org,
        is_admin_org,
        is_admin,
        is_superadmin,
    ) = definerights(request, currentticket.company_id)

    button_feedbackticket_update = ""
    button_ticketcomment_create = ""

    if currentuser == currentticket.author_id or is_support_member:  # or is_member:
        button_ticketcomment_create = _("Создать")
        # if currentuser == currentticket.author_id:
        button_feedbackticket_update = _("Изменить")
    button_feedbacktask_create = ""
    if (
        currentticket.company_id in request.session["_auth_user_companies_id"]
        or is_support_member
    ):
        button_feedbacktask_create = _("Создать")

    is_system_dev = request.session["system_dev"][1]
    try:
        current_companyid = request.session["_auth_user_supportcompany_id"]
    except:
        current_companyid = 0

    # task_list.refresh_from_db()
    # print(is_ticketslist_dev)

    return render(
        request,
        "feedbackticket_detail.html",
        {
            "nodes": task_list.distinct(),
            "ticketcommentnodes": ticketcomment_list.distinct().order_by(),
            # "len_list": len_list,
            # "is_system_dev": is_system_dev,
            "current_task": current_task,
            "root_task_id": root_task_id,
            "tree_task_id": tree_task_id,
            "is_support_member": is_support_member,
            "current_feedbackticket": currentticket,
            "current_company": currentticket.company,
            "current_companyid": current_companyid,
            "ticketid": ticketid,
            "current_ticketid": ticketid,
            "user_companies": request.session["_auth_user_companies_id"],
            "obj_files_rights": obj_files_rights,
            "files": FeedbackFile.objects.filter(ticket=currentticket, is_active=True)
            .select_related("author", "ticket", "ticketcomment", "task", "taskcomment")
            .order_by("uname"),
            "objtype": "fbtsk",
            "media_path": settings.MEDIA_URL,
            # 'button_client_create': button_client_create,
            "button_feedbackticket_update": button_feedbackticket_update,
            # 'button_client_history': button_client_history,
            "button_feedbacktask_create": button_feedbacktask_create,
            "button_ticketcomment_create": button_ticketcomment_create,
            "taskstatus": Dict_FeedbackTaskStatus.objects.filter(is_active=True),
            "tskstatus_selectid": tskstatus_selectid,
            "tskstatus_myselectid": tskstatus_myselectid,
            "is_system_dev": request.session["system_dev"][1],
            "is_ticketslist_dev": is_ticketslist_dev,
            "object_list": "feedbacktask_list",
            "ticketcomment_costsum": ticketcomment_costsum,
            "task_costsum": task_costsum,
            "taskcomment_costsum": taskcomment_costsum,
            "taskcomment_timesum": taskcomment_timesum,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
        },
    )


class FeedbackTicketCommentCreate(AddFilesMixin, CreateView):
    model = FeedbackTicketComment
    form_class = FeedbackTicketCommentForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(FeedbackTicketCommentCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новый комментарий Тикета")
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # is_support_member = self.request.session['_auth_user_issupportmember']
        is_support_member = False
        if len(self.request.session["_auth_user_compsupportid"]) > 0:
            is_support_member = True
        is_ticketslist_dev = self.kwargs["is_ticketslist_dev"]
        kwargs.update(
            {
                "is_support_member": is_support_member,
                "is_ticketslist_dev": is_ticketslist_dev,
            }
        )
        return kwargs

    def form_valid(self, form):
        form.instance.ticket_id = self.kwargs["ticketid"]
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новый коммент Тикета
        af = self.add_files(
            form, "feedback", "ticketcomment"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        # отправляем коммент удалённому автору тикета
        # print('/',str(form.instance.ticket.id_remote),'/')
        # sys = Dict_System.objects.filter(id=form.instance.ticket.system_id).first()
        sys = Dict_System.objects.filter(id=form.instance.ticket.system_id).first()
        sysloc = Dict_System.objects.filter(is_active=True, is_local=True).first()
        # if form.instance.ticket.company_id == None:
        if sys.is_local == False:
            # отправляем коммент разработчику
            # print(sysloc)
            headers = {"Content-type": "application/json", "Accept": "application/json"}
            # ticket_data = {'name': form.instance.name, 'description': form.instance.description, 'ticketid': str(form.instance.ticket.id_remote)}
            ticket_data = {
                "name": form.instance.name,
                "description": form.instance.description,
                "systemcode": sysloc.code,
                "ticketid": str(form.instance.ticket_id),
                "id_remote": str(self.object.id),
            }
            url_dev = form.instance.ticket.system.url + "/feedback/api/ticketcomment/"
            r = requests.post(url_dev, headers=headers, data=json.dumps(ticket_data))
            if af and r.status_code < 300:
                # *** отправляем вдогонку файлы ***
                files = FeedbackFile.objects.filter(ticketcomment_id=self.object.id)
                fl = []
                for f in files:
                    fl.append(
                        (
                            "feedbackticket_file",
                            (
                                str(f.name),
                                open(settings.MEDIA_ROOT + "/" + str(f.pfile), "rb"),
                            ),
                        )
                    )
                    # print(fl)
                url_dev = sys.url + "/feedback/api/file/"
                dt = {
                    "ticketid": str(form.instance.ticket_id),
                    "ticketcommentid": str(self.object.id),
                }
                r_f = requests.request("POST", url_dev, headers={}, data=dt, files=fl)
                print(r_f.text, dt, fl)
            # print(r)
            self.object.id_remote = r.json()["id"]
            self.object.requeststatuscode = r.status_code
            self.object = form.save()
        return super().form_valid(form)


class FeedbackTaskCreate(AddFilesMixin, CreateView):
    model = FeedbackTask
    form_class = FeedbackTaskForm
    # template_name = 'task_create.html'
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.ticket_id = self.kwargs["ticketid"]
        if self.kwargs["parentid"] != 0:
            form.instance.parent_id = self.kwargs["parentid"]
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новую задачу Тикета
        af = self.add_files(
            form, "feedback", "task"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FeedbackTaskCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новая Задача")
        return context

    def get_form_kwargs(self):
        kwargs = super(FeedbackTaskCreate, self).get_form_kwargs()
        kwargs.update(
            {
                "user": self.request.user,
                "action": "create",
                "companyid": self.kwargs["companyid"],
                "ticketid": self.kwargs["ticketid"],
            }
        )
        return kwargs


class FeedbackTaskUpdate(AddFilesMixin, UpdateView):
    model = FeedbackTask
    form_class = FeedbackTaskForm
    # template_name = 'task_update.html'
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(FeedbackTaskUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Задачу")
        context["files"] = FeedbackFile.objects.filter(
            task_id=self.kwargs["pk"], is_active=True
        ).order_by("uname")
        return context

    def get_form_kwargs(self):
        kwargs = super(FeedbackTaskUpdate, self).get_form_kwargs()
        kwargs.update({"user": self.request.user, "action": "update"})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        af = self.add_files(
            form, "feedback", "task"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        old = FeedbackTask.objects.filter(
            pk=self.object.pk
        ).first()  # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта

        return super().form_valid(form)


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def feedbacktaskcomments(request, taskid):
    currenttask = (
        FeedbackTask.objects.filter(id=taskid)
        .select_related(
            "ticket",
            "ticket__company",
            "ticket__company__currency",
            "author",
            "assigner",
            "status",
        )
        .first()
    )
    currentuser = request.user.id
    if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id:
        obj_files_rights = 1
    else:
        obj_files_rights = 0

    # taskcomment_costsum = FeedbackTaskComment.objects.filter(task=taskid).aggregate(Sum('cost'))
    # taskcomment_timesum = FeedbackTaskComment.objects.filter(task=taskid).aggregate(Sum('time'))
    taskcomment_costsum = currenttask.costsum
    taskcomment_timesum = currenttask.timesum

    try:
        sec = taskcomment_timesum["time__sum"] * 3600
    except:
        sec = 0
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    seconds = sec
    taskcomment_list = FeedbackTaskComment.objects.filter(
        Q(author=request.user.id), is_active=True, task=taskid
    ).select_related(
        "task",
        "task__ticket",
        "task__ticket__company",
        "task__ticket__company__currency",
        "author",
    )

    # event_list = ClientEvent.objects.filter(task=currenttask, is_active=True)
    is_ticketslist_dev = 0
    currentticket = (
        FeedbackTicket.objects.filter(id=currenttask.ticket_id)
        .select_related("system", "company", "companyfrom", "author", "type", "status")
        .first()
    )
    if currentticket.company_id == None:
        is_ticketslist_dev = 1

    # print(taskcomment_list)
    button_taskcomment_create = ""
    # button_taskcomment_update = ''
    button_task_create = ""
    button_task_update = ""
    button_task_history = ""
    # print(currentuser, currenttask.author_id, currenttask.assigner_id)
    if (
        currentuser == currenttask.author_id or currentuser == currenttask.assigner_id
    ):  # or is_member:
        button_task_create = _("Добавить")
        # button_task_history = _('История')
        button_taskcomment_create = _("Добавить")
        if (
            currentuser == currenttask.author_id
            or currentuser == currenttask.assigner_id
        ):
            button_task_update = _("Изменить")

    try:
        current_companyid = request.session["_auth_user_supportcompany_id"]
    except:
        current_companyid = 0

    return render(
        request,
        "feedbacktask_detail.html",
        {
            "nodes": taskcomment_list.distinct().order_by(),
            # 'current_taskcomment': currenttaskcomment,
            "task": currenttask,
            "current_companyid": current_companyid,
            "is_ticketslist_dev": is_ticketslist_dev,
            "obj_files_rights": obj_files_rights,
            "files": FeedbackFile.objects.filter(task=currenttask, is_active=True)
            .select_related("author", "ticket", "ticketcomment", "task", "taskcomment")
            .order_by("uname"),
            "objtype": "fbtsk",
            "button_task_create": button_task_create,
            "button_task_update": button_task_update,
            #'button_task_history': button_task_history,
            #'object_list': 'clienttask_list',
            "taskcomment_costsum": taskcomment_costsum,
            "taskcomment_timesum": taskcomment_timesum,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "button_taskcomment_create": button_taskcomment_create,
            #'enodes': event_list.distinct().order_by(),
            #'button_event_create': button_event_create,
            "media_path": settings.MEDIA_URL,
        },
    )


class FeedbackTaskCommentDetail(DetailView):
    model = FeedbackTaskComment
    template_name = "taskcomment_detail.html"


class FeedbackTaskCommentCreate(AddFilesMixin, CreateView):
    model = FeedbackTaskComment
    form_class = FeedbackTaskCommentForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(FeedbackTaskCommentCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новый Комментарий")
        return context

    def form_valid(self, form):
        form.instance.task_id = self.kwargs["taskid"]
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новый коммент задачи клиента
        af = self.add_files(
            form, "feedback", "taskcomment"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        return super(FeedbackTaskCommentCreate, self).form_valid(form)


class FeedbackTaskCommentUpdate(UpdateView):
    model = FeedbackTaskComment
    # form_class = FeedbackTaskCommentForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(FeedbackTaskCommentUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Комментарий")
        context["files"] = FeedbackFile.objects.filter(
            taskcomment_id=self.kwargs["pk"], is_active=True
        ).order_by("uname")
        return context


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def ticketfilter(request):
    # systemid = request.GET['systemid']
    companyid = request.GET["companyid"]
    statusid = request.GET["statusid"]
    typeid = request.GET["typeid"]
    try:
        myticketuser = request.GET["my"]
    except:
        myticketuser = "0"
    is_ticketslist_dev = int(request.GET["is_ticketslist_dev"])

    currentuser = request.user.id

    # print(companyid, currentuser, statusid, typeid, mytskuser, is_ticketslist_dev)

    current_company = Company.objects.filter(id=companyid).first()
    """
        if companyid == 0:
            companyid = request.session['_auth_user_currentcompany_id']


        #ticket_list = FeedbackTicket.objects.filter(is_active=True, system_id=systemid, company_id=companyid)
        ticket_list = FeedbackTicket.objects.filter(is_active=True, company_id=companyid)

        # *** фильтруем по статусу ***
        if statusid == "0":
            ticket_list = ticket_list.filter(dateclose__isnull=True)
        elif statusid == "-2":
            ticket_list = ticket_list.filter(dateclose__lte=datetime.now())
        elif statusid != "-1":
            ticket_list = ticket_list.filter(status_id=statusid)

        # *** фильтруем по типу ***
        if typeid != "-1":
            ticket_list = ticket_list.filter(type_id=typeid)
        # *** фильтр по принадлежности ***
        if mytskuser == "1":
            #ticket_list = ticket_list.filter(author_id=currentuser)
            ticket_list = ticket_list.filter(Q(author=request.user.id))
        # **********
        """
    (
        is_support_member,
        is_support_admin_org,
        is_admin_org,
        is_admin,
        is_superadmin,
    ) = definerights(request, companyid)
    # print(is_support_member, is_support_admin_org, is_admin_org, is_admin, is_superadmin)
    # currentusercompanyid = request.session['_auth_user_currentcompany_id']
    systemdevid = request.session["system_dev"][0]
    is_system_dev = request.session["system_dev"][1]

    feedbackticket_list = FeedbackTicket.objects.filter(is_active=True).select_related(
        "system",
        "author",
        "company",
        "company__currency",
        "companyfrom",
        "type",
        "status",
    )

    if is_ticketslist_dev == 1:
        # список тикетов разработчику
        if is_system_dev:
            # список тикетов разработчику в системе разработчика 1YES!
            feedbackticket_list = feedbackticket_list.filter(system_id=systemdevid)
        else:
            # список тикетов разработчику в локальной системе
            feedbackticket_list = feedbackticket_list.filter(
                system_id=systemdevid, company_id__isnull=True, companyfrom_id=companyid
            )
        template_name = "feedbackticketsdev_list.html"
        # print("************************", feedbackticket_list)
    else:
        # список тикетов внутри системы
        feedbackticket_list = feedbackticket_list.filter(company=companyid).exclude(
            system=systemdevid
        )
        template_name = "feedbacktickets_list.html"

    # *** фильтруем по статусу ***
    if statusid == "0":
        feedbackticket_list = feedbackticket_list.filter(dateclose__isnull=True)
    elif statusid == "-2":
        feedbackticket_list = feedbackticket_list.filter(dateclose__lte=datetime.now())
    elif statusid != "-1":
        feedbackticket_list = feedbackticket_list.filter(status_id=statusid)

    # *** фильтруем по типу ***
    if typeid != "-1":
        feedbackticket_list = feedbackticket_list.filter(type_id=typeid)

    # *** фильтр по принадлежности ***
    if myticketuser == "1":
        # ticket_list = ticket_list.filter(author_id=currentuser)
        feedbackticket_list = feedbackticket_list.filter(Q(author=request.user.id))
    # **********

    # print(companyid, currentuser, statusid, typeid, myticketuser, is_ticketslist_dev)
    # nodes = ticket_list.distinct() #.order_by()
    nodes = feedbackticket_list.distinct()  # .order_by()
    # print(ticket_list, nodes)
    # status_list = ticket_list.values('status_id')
    # ticketstatus = Dict_FeedbackTicketStatus.objects.filter(id__in=status_list)
    # types_list = ticket_list.values('type_id')
    # tickettype = Dict_FeedbackTicketType.objects.filter(id__in=types_list)
    ticketstatus = Dict_FeedbackTicketStatus.objects.filter(is_active=True)
    tickettype = Dict_FeedbackTicketType.objects.filter(is_active=True)
    # print(statuss_list, ticketstatus)
    # print(systemid, companyid, ticket_list)

    button_feedbackticket_create = _("Добавить")

    len_list = len(nodes)
    object_message = ""
    if len_list == 0:
        object_message = _("Тикеты не найдены!")

    return render(
        request,
        template_name,
        {
            "nodes_tickets": nodes,
            "object_list": "feedbacktask_list",
            "systemdevid": systemdevid,
            "companyid": companyid,
            "len_list": len_list,
            "current_company": current_company,
            "current_ticketid": 0,
            "object_message": object_message,
            "ticketstatus": ticketstatus,
            "tickettype": tickettype,
            "myticketselectid": myticketuser,
            "is_ticketslist_dev": is_ticketslist_dev,
            "button_feedbackticket_create": button_feedbackticket_create,
            "button_feedbackticketdev_create": button_feedbackticket_create,
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def tickettaskfilter(request):
    companyid = request.GET["companyid"]
    ticketid = request.GET["ticketid"]
    statusid = request.GET["statusid"]
    # mytskuser = request.GET['my']
    try:
        mytskuser = request.GET["my"]
    except:
        mytskuser = "0"
    is_ticketslist_dev = int(request.GET["is_ticketslist_dev"])

    # currentuser = request.user.id
    current_company = Company.objects.filter(id=companyid).first()
    current_ticketid = 0
    if ticketid != "0":
        current_ticket = (
            FeedbackTicket.objects.filter(id=ticketid)
            .select_related(
                "system",
                "author",
                "company",
                "company__currency",
                "companyfrom",
                "type",
                "status",
            )
            .first()
        )
        current_ticketid = current_ticket.id

    tickettask_list = tickettasklist(
        request, companyid, ticketid, statusid, mytskuser, is_ticketslist_dev
    )

    nodes = tickettask_list.distinct()
    taskstatus = Dict_FeedbackTaskStatus.objects.filter(is_active=True)

    len_list = len(nodes)
    object_message = ""
    if len_list == 0:
        object_message = _("Задачи не найдены!")

    return render(
        request,
        "objects_list.html",
        {
            "nodes": nodes,
            "current_company": current_company,
            "current_ticketid": current_ticketid,
            "len_list": len_list,
            "object_list": "feedbacktask_list",
            "object_message": object_message,
            "tskstatus_selectid": taskstatus,
            "tskstatus_myselectid": mytskuser,
            "is_ticketslist_dev": is_ticketslist_dev,
        },
    )


def tickettasklist(
    request, companyid, ticketid="0", statusid="0", mytskuser="0", is_ticketslist_dev=0
):
    tickettask_list = FeedbackTask.objects.filter(is_active=True).select_related(
        "ticket",
        "ticket__company",
        "ticket__company__currency",
        "status",
        "assigner",
        "author",
    )
    if ticketid == "0":
        if is_ticketslist_dev == 1:
            tickettask_list = tickettask_list.filter(ticket__company_id__isnull=True)
        else:
            tickettask_list = tickettask_list.filter(ticket__company_id=companyid)
        # current_ticketid = 0
    else:
        # current_ticket = FeedbackTicket.objects.filter(id=ticketid).first()
        # current_ticketid = current_ticket.id
        tickettask_list = tickettask_list.filter(ticket_id=ticketid)

    # *** фильтруем по статусу ***
    if statusid == "0":
        tickettask_list = tickettask_list.filter(dateclose__isnull=True)
    elif statusid == "-2":
        tickettask_list = tickettask_list.filter(
            dateclose__isnull=True, dateend__lte=datetime.now()
        )
    elif statusid != "-1":
        tickettask_list = tickettask_list.filter(status_id=statusid)
    # **********
    # print(tickettask_list)
    # *** фильтр по принадлежности ***
    if mytskuser == "1":
        tickettask_list = tickettask_list.filter(Q(author=request.user.id))
    elif mytskuser == "2":
        tickettask_list = tickettask_list.filter(Q(assigner=request.user.id))
    elif mytskuser == "3":
        tickettask_list = tickettask_list.filter(
            Q(author=request.user.id) | Q(assigner=request.user.id)
        )
    # *******************************

    return tickettask_list


# for Dashboard
def feedback_tickets_tasks(request):
    currentuser = request.user.id
    companies_id = request.session["_auth_user_companies_id"]
    date_end = datetime.now() + timedelta(days=10)
    # print('timedelta={}'.format(timedelta(days=10)))
    # print(request, date_end)

    feedback_tickets_list = (
        FeedbackTicket.objects.filter(
            Q(company__in=companies_id)
            | Q(companyfrom__in=companies_id)
            | Q(author=request.user.id),
            is_active=True,
            status__is_close=False,
            dateclose__isnull=True,
        )
        .select_related("company", "companyfrom", "system", "type", "status", "author")
        .order_by("datecreate", "type")
        .distinct()
    )

    feedback_tasks_list = (
        FeedbackTask.objects.filter(
            Q(ticket__author=request.user.id)
            | Q(assigner=request.user.id)
            | Q(author=request.user.id),
            is_active=True,
            status__is_close=False,
            dateclose__isnull=True,
            dateend__lte=date_end,
        )
        .select_related(
            "ticket", "ticket__company__currency", "status", "assigner", "author"
        )
        .order_by("dateend", "status")
        .distinct()
    )

    # print(projects_list, projects_tasks_list)

    return (feedback_tickets_list, feedback_tasks_list)
