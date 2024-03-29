from django.conf import settings
from datetime import datetime, timedelta  # , timezone #date, time
import json

from companies.models import Company
from main.models import ModelLog
from crm.models import Client, Dict_ClientStatus, Dict_ClientType
from crm.models import (
    ClientTask,
    ClientTaskComment,
    Dict_ClientTaskStatus,
    Dict_ClientTaskType,
)  # , ClientStatusLog, ClientTaskStatusLog
from crm.models import (
    ClientEvent,
    ClientEventComment,
    Dict_ClientEventStatus,
    Dict_ClientEventType,
    ClientFile,
)  # , ClientEventStatusLog

from .forms import ClientForm, ClientTaskForm, ClientTaskCommentForm
from .forms import ClientEventForm, ClientEventCommentForm

from django.contrib.auth.decorators import login_required

from main.utils import AddFilesMixin

from django.utils.translation import gettext_lazy as _

# # not used
# import os
# from django.urls import reverse_lazy
# from django.utils import timezone
# from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
# from django.template import loader, Context, RequestContext
# from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render  # , redirect, get_object_or_404

# View, TemplateView, ListView,
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import UpdateView  # , DeleteView
from django.db.models import Q, Sum  # , Count, Min, Max, Avg

# from versane.models import Company
# import socket
# from clients.models import Dict_clientStatus, Dict_TaskStatus
# from companies.forms import CompanyForm
# from .tables import ClientTable, ClientStatusLogTable, ClientTaskStatusLogTable, ClientEventStatusLogTable
# from projects.tables import ProjectStatusLogTable
# from django_tables2 import RequestConfig


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clients(request, companyid=0, pk=0):
    if companyid == 0:
        companyid = request.session["_auth_user_currentcompany_id"]

    request.session["_auth_user_currentcomponent"] = "crm"

    # *** фильтруем по статусу ***
    currentuser = request.user.id
    clntstatus_selectid = 0
    # myclntstatus = 0 # для фильтра "Мои клиенты"
    try:
        clntstatus = request.POST["select_clientstatus"]
    except:
        client_list = Client.objects.filter(
            Q(author=request.user.id)
            | Q(manager=request.user.id)
            | Q(
                members__in=[
                    currentuser,
                ]
            ),
            is_active=True,
            company=companyid,
            dateclose__isnull=True,
        )
    else:
        if clntstatus == "0":
            # если в выпадающем списке выбрано "Все активные"
            client_list = Client.objects.filter(
                Q(author=request.user.id)
                | Q(manager=request.user.id)
                | Q(
                    members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                company=companyid,
                dateclose__isnull=True,
            )
        else:
            if clntstatus == "-1":
                # если в выпадающем списке выбрано "Все"
                client_list = Client.objects.filter(
                    Q(author=request.user.id)
                    | Q(manager=request.user.id)
                    | Q(
                        members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    company=companyid,
                )
            elif clntstatus == "-2":
                # если в выпадающем списке выбрано "Просроченные"
                client_list = Client.objects.filter(
                    Q(author=request.user.id)
                    | Q(manager=request.user.id)
                    | Q(
                        members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    company=companyid,
                    dateclose__isnull=True,
                    dateend__lt=datetime.now(),
                )
            else:
                client_list = Client.objects.filter(
                    Q(author=request.user.id)
                    | Q(manager=request.user.id)
                    | Q(
                        members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    company=companyid,
                    status=clntstatus,
                )  # , dateclose__isnull=True)
        clntstatus_selectid = clntstatus
    # clntstatus_myselectid = myclntstatus
    # *******************************
    # client_list = client_list.order_by('dateclose')

    client_list = client_list.select_related(
        "company",
        "manager",
        "user",
        "protocoltype",
        "type",
        "status",
        "currency",
        "initiator",
        "author",
    )

    len_list = len(client_list)

    current_company = Company.objects.get(id=companyid)
    obj_files_rights = 0

    if pk == 0:
        current_client = 0
        # tree_client_id = 0
        # root_client_id = 0
    else:
        current_client = Client.objects.get(id=pk)
        if (
            currentuser == current_client.author_id
            or currentuser == current_client.manager_id
        ):
            obj_files_rights = 1
        # tree_client_id = current_client.tree_id
        # root_client_id = current_client.get_root().id

    button_company_select = ""
    button_company_create = ""
    button_company_update = ""
    button_client_create = ""

    # здесь нужно условие для button_company_create
    # если текущий пользователь не является автором созданной текущей организации, то добавлять и изменять Компанию можно только в приложении Организации
    # button_company_create = 'Добавить'
    # здесь нужно условие для button_company_update
    # button_company_update = 'Изменить'
    # здесь нужно условие для button_client_create
    # button_client_create = 'Добавить'
    # здесь нужно условие для button_company_select
    comps = request.session["_auth_user_companies_id"]
    if len(comps) > 1:
        button_company_select = _("Сменить организацию")
    if currentuser == current_company.author_id:
        button_company_create = button_client_create = _("Добавить")
        button_company_update = _("Изменить")
        # button_client_create = _("Добавить")
    if current_company in comps:
        button_client_create = button_company_create  # _("Добавить")
    nodes = client_list.distinct().order_by()
    # table = ClientTable(nodes, c1_name='Клиент')
    # table = ClientTable(nodes)
    return render(
        request,
        "company_detail.html",
        {
            "nodes": nodes,
            "current_client": current_client,
            "current_company": current_company,
            "companyid": companyid,
            "user_companies": comps,
            "obj_files_rights": obj_files_rights,
            # 'objtype': 'clnt',
            # 'files': ClientFile.objects.filter(client=currentclient, is_active=True).order_by('uname'),
            # 'media_path': settings.MEDIA_URL,
            "button_company_select": button_company_select,
            "button_company_create": button_company_create,
            "button_company_update": button_company_update,
            "button_client_create": button_client_create,
            # 'button_client_history': button_client_history,
            "clientstatus": Dict_ClientStatus.objects.filter(is_active=True),
            "clienttype": Dict_ClientType.objects.filter(is_active=True),
            "clntstatus_selectid": clntstatus_selectid,
            # 'clntstatus_myselectid': clntstatus_myselectid,
            "object_list": "client_list",
            # 'select_clientstatus': select_clientstatus,
            "component_name": "crm",
            # 'table': table,
            "len_list": len_list,
        },
    )


class ClientCreate(AddFilesMixin, CreateView):
    model = Client
    form_class = ClientForm
    # template_name = 'client_create.html'
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.company_id = self.kwargs["companyid"]
        # if self.kwargs['parentid'] != 0:
        #   form.instance.parent_id = self.kwargs['parentid']
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём нового клиента
        af = self.add_files(
            form, "crm", "client"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        # Делаем первую запись в историю изменений проекта
        self_user_username = ""
        if self.object.user:
            self_user_username = self.object.user.username
        self_object_protocoltype_name = ""
        if self.object.protocoltype:
            self_object_protocoltype_name = self.object.protocoltype.name
        # формируем строку из Участников
        memb = self.object.members.values_list("id", "username").all()
        membersstr = ""
        for mem in memb:
            membersstr = membersstr + mem[1] + ","
        historyjson = {
            str(_("Имя")): self.object.firstname,
            str(_("Отчество")): self.object.middlename,
            str(_("Фамилия")): self.object.lastname,
            str(_("Пользователь")): "-"
            if self_user_username == ""
            else self_user_username,
            "E-mail": self.object.email,
            str(_("Телефон")): self.object.phone,
            str(_("Тип")): self.object.type.name,
            str(_("Статус")): self.object.status.name,
            str(_("Ст-ть")): str(self.object.cost),
            str(_("Валюта")): self.object.currency.code_char,
            str(_("Выполнен на, %")): str(self.object.percentage),
            str(_("Инициатор")): self.object.initiator.name,
            str(_("Менеджер")): self.object.manager.username,
            str(_("Участники")): membersstr,
            str(_("Оповещ.")): "✓" if self.object.is_notify else "-",
            str(_("Протокол")): "-"
            if self_object_protocoltype_name == ""
            else self_object_protocoltype_name,
            str(_("Активн.")): "✓" if self.object.is_active else "-",
        }
        ModelLog.objects.create(
            componentname="clnt",
            modelname="Client",
            modelobjectid=self.object.id,
            author=self.object.author,
            log=json.dumps(historyjson),
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClientCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новый Клиент")
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # здесь нужно условие для 'action': 'create'
        kwargs.update(
            {
                "user": self.request.user,
                "action": "create",
                "companyid": self.kwargs["companyid"],
            }
        )
        return kwargs


class ClientUpdate(AddFilesMixin, UpdateView):
    model = Client
    form_class = ClientForm
    # template_name = 'client_update.html'
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(ClientUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Клиента")
        context["files"] = ClientFile.objects.filter(
            client_id=self.kwargs["pk"], is_active=True
        ).order_by("uname")
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # здесь нужно условие для 'action': 'update'
        kwargs.update({"user": self.request.user, "action": "update"})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(
            commit=False
        )  # без commit=False происходит вызов save() Модели
        af = self.add_files(
            form, "crm", "client"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        old = Client.objects.filter(
            pk=self.object.pk
        ).first()  # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
        old_user_username = ""
        self_user_username = ""
        if old.user:
            old_user_username = old.user.username
        if self.object.user:
            self_user_username = self.object.user.username
        # обрабатываем изменения Участников
        # старые Участники
        old_memb = old.members.values_list("id", "username").all()
        old_memb_count = old_memb.count()
        old_memb_list = list(old_memb)
        self.object = form.save()
        # новые Участники
        memb = self.object.members.values_list("id", "username").all()
        memb_count = memb.count()
        is_members_changed = False
        if old_memb_count != memb_count:
            is_members_changed = True
        # print(list(memb))
        # формируем строку из новых Участников и признак их изменения
        membersstr = ""
        for mem in memb:
            membersstr = membersstr + mem[1] + ","
            if not is_members_changed:
                if old_memb_list.count(mem) == 0:
                    is_members_changed = True

        historyjson = {
            str(_("Имя")): ""
            if self.object.firstname == old.firstname
            else self.object.firstname,
            str(_("Отчество")): ""
            if self.object.middlename == old.middlename
            else self.object.middlename,
            str(_("Фамилия")): ""
            if self.object.lastname == old.lastname
            else self.object.lastname,
            str(_("Пользователь")): ""
            if self_user_username == old_user_username
            else "-"
            if self_user_username == ""
            else self_user_username,
            str(_("E-mail")): ""
            if self.object.email == old.email
            else self.object.email,
            str(_("Телефон")): ""
            if self.object.phone == old.phone
            else self.object.phone,
            str(_("Тип")): ""
            if self.object.type.name == old.type.name
            else self.object.type.name,
            str(_("Статус")): ""
            if self.object.status.name == old.status.name
            else self.object.status.name,
            str(_("Ст-ть")): ""
            if self.object.cost == old.cost
            else str(self.object.cost),
            str(_("Валюта")): ""
            if self.object.currency.code_char == old.currency.code_char
            else self.object.currency.code_char,
            str(_("Выполнен на, %")): ""
            if self.object.percentage == old.percentage
            else str(self.object.percentage),
            str(_("Инициатор")): ""
            if self.object.initiator.name == old.initiator.name
            else self.object.initiator.name,
            str(_("Менеджер")): ""
            if self.object.manager.username == old.manager.username
            else self.object.manager.username,
            str(_("Участники")): "" if is_members_changed is False else membersstr,
            str(_("Оповещ.")): ""
            if self.object.is_notify == old.is_notify
            else "✓"
            if self.object.is_notify
            else "-",
            str(_("Протокол")): ""
            if self.object.protocoltype.name == old.protocoltype.name
            else self.object.protocoltype.name,
            str(_("Активн.")): ""
            if self.object.is_active == old.is_active
            else "✓"
            if self.object.is_active
            else "-",
        }
        ModelLog.objects.create(
            componentname="clnt",
            modelname="Client",
            modelobjectid=self.object.id,
            author=self.object.author,
            log=json.dumps(historyjson),
        )
        return super().form_valid(form)  # super(ProjectUpdate, self).form_valid(form)


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienttasks(request, clientid=0, pk=0):
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    tskstatus_selectid = 0
    try:
        tskstatus = request.POST["select_taskstatus"]
    except:
        task_list = ClientTask.objects.filter(
            Q(author=request.user.id)
            | Q(assigner=request.user.id)
            | Q(
                client__members__in=[
                    currentuser,
                ]
            ),
            is_active=True,
            client=clientid,
            dateclose__isnull=True,
        )
    else:
        if tskstatus == "0":
            # если в выпадающем списке выбрано "Все активные"
            task_list = ClientTask.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    client__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                client=clientid,
                dateclose__isnull=True,
            )
        else:
            if tskstatus == "-1":
                # если в выпадающем списке выбрано "Все"
                task_list = ClientTask.objects.filter(
                    Q(author=request.user.id)
                    | Q(assigner=request.user.id)
                    | Q(
                        client__members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    client=clientid,
                )
            elif tskstatus == "-2":
                # если в выпадающем списке выбрано "Просроченные"
                task_list = ClientTask.objects.filter(
                    Q(author=request.user.id)
                    | Q(assigner=request.user.id)
                    | Q(
                        client__members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    client=clientid,
                    dateclose__isnull=True,
                    dateend__lt=datetime.now(),
                )
            else:
                task_list = ClientTask.objects.filter(
                    Q(author=request.user.id)
                    | Q(assigner=request.user.id)
                    | Q(
                        client__members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    client=clientid,
                    status=tskstatus,
                )  # , dateclose__isnull=True)
        tskstatus_selectid = tskstatus
    # *******************************

    # len_list = len(task_list)

    event_list = ClientEvent.objects.filter(client=clientid, is_active=True)
    # len_elist = len(event_list)

    currentclient = (
        Client.objects.filter(id=clientid)
        .select_related(
            "company",
            "manager",
            "user",
            "protocoltype",
            "type",
            "status",
            "currency",
            "initiator",
            "author",
        )
        .first()
    )

    taskcomment_costsum = ClientTaskComment.objects.filter(
        task__client_id=currentclient.id
    ).aggregate(Sum("cost"))
    taskcomment_timesum = ClientTaskComment.objects.filter(
        task__client_id=currentclient.id
    ).aggregate(Sum("time"))
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
        tree_task_id = 0
        root_task_id = 0
        tree_task_id = 0
        if (
            currentuser == currentclient.author_id
            or currentuser == currentclient.manager_id
        ):
            obj_files_rights = 1
    else:
        current_task = (
            ClientTask.objects.filter(id=pk)
            .select_related(
                "client",
                "assigner",
                "structure_type",
                "type",
                "status",
                "author",
                "initiator",
            )
            .first()
        )
        tree_task_id = current_task.tree_id
        root_task_id = current_task.get_root().id
        tree_task_id = current_task.tree_id
        if (
            currentuser == current_task.author_id
            or currentuser == current_task.assigner_id
        ):
            obj_files_rights = 1

    button_client_create = ""
    button_client_update = ""
    button_client_history = ""
    button_task_create = ""

    is_member = Client.objects.filter(
        members__in=[
            currentuser,
        ]
    ).exists()
    if (
        currentuser == currentclient.author_id
        or currentuser == currentclient.manager_id
        or is_member
    ):
        # button_client_create = 'Добавить'
        button_client_history = _("История")
        button_task_create = button_event_create = _("Добавить")
        # button_event_create = _("Добавить")
        if (
            currentuser == currentclient.author_id
            or currentuser == currentclient.manager_id
        ):
            button_client_update = _("Изменить")

    task_list = task_list.select_related(
        "client", "assigner", "structure_type", "type", "status", "author", "initiator"
    )
    event_list = event_list.select_related("client", "task", "type", "status")

    return render(
        request,
        "client_detail.html",
        {
            "nodes":
            # task_list.distinct().order_by(),
            task_list.distinct(),  # .order_by('tree_id', 'level', 'dateend'),
            "current_task": current_task,
            "root_task_id": root_task_id,
            "tree_task_id": tree_task_id,
            "current_client": currentclient,
            "clientid": clientid,
            "user_companies": request.session["_auth_user_companies_id"],
            "obj_files_rights": obj_files_rights,
            "files": ClientFile.objects.filter(
                client=currentclient, is_active=True
            ).order_by("uname"),
            "objtype": "clnt",
            "media_path": settings.MEDIA_URL,
            "button_client_create": button_client_create,
            "button_client_update": button_client_update,
            "button_client_history": button_client_history,
            "button_task_create": button_task_create,
            # 'button_task_history': button_task_history,
            "taskstatus": Dict_ClientTaskStatus.objects.filter(is_active=True),
            "tasktype": Dict_ClientTaskType.objects.filter(is_active=True),
            "tskstatus_selectid": tskstatus_selectid,
            "object_list": "clienttask_list",
            "taskcomment_costsum": taskcomment_costsum,
            "taskcomment_timesum": taskcomment_timesum,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            # 'len_list': len_list,
            "enodes": event_list.distinct().order_by(),
            # 'len_elist': len_elist,
            "button_event_create": button_event_create,
            "eventstatus": Dict_ClientEventStatus.objects.filter(is_active=True),
            "eventtype": Dict_ClientEventType.objects.filter(is_active=True),
            # 'evntstatus_selectid': evntstatus_selectid,
        },
    )


class ClientTaskCreate(AddFilesMixin, CreateView):
    model = ClientTask
    form_class = ClientTaskForm
    # template_name = 'task_create.html'
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.client_id = self.kwargs["clientid"]
        if self.kwargs["parentid"] != 0:
            form.instance.parent_id = self.kwargs["parentid"]
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новую задачу клиента
        af = self.add_files(
            form, "crm", "task"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        historyjson = {
            str(_("Задача")): self.object.name,
            str(_("Статус")): self.object.status.name,
            str(_("Начало")): self.object.datebegin.strftime("%d.%m.%Y %H:%M"),
            str(_("Окончание")): self.object.dateend.strftime("%d.%m.%Y %H:%M"),
            str(_("Тип в иерархии")): self.object.structure_type.name,
            str(_("Тип")): self.object.type.name,
            str(_("Стоимость")): str(self.object.cost),
            str(_("Выполнен на, %")): str(self.object.percentage),
            str(_("Инициатор")): self.object.initiator.name,
            str(_("Исполнитель")): self.object.assigner.username,
            str(_("Активность")): "✓" if self.object.is_active else "-"
            # , str(_("Участники")):self.object.members.username
        }
        ModelLog.objects.create(
            componentname="cltsk",
            modelname="ClientTask",
            modelobjectid=self.object.id,
            author=self.object.author,
            log=json.dumps(historyjson),
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClientTaskCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новая Задача")
        return context

    def get_form_kwargs(self):
        kwargs = super(ClientTaskCreate, self).get_form_kwargs()
        kwargs.update(
            {
                "user": self.request.user,
                "action": "create",
                "clientid": self.kwargs["clientid"],
            }
        )
        return kwargs


class ClientTaskUpdate(AddFilesMixin, UpdateView):
    model = ClientTask
    form_class = ClientTaskForm
    # template_name = 'task_update.html'
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(ClientTaskUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Задачу")
        context["files"] = ClientFile.objects.filter(
            task_id=self.kwargs["pk"], is_active=True
        ).order_by("uname")
        return context

    def get_form_kwargs(self):
        kwargs = super(ClientTaskUpdate, self).get_form_kwargs()
        kwargs.update({"user": self.request.user, "action": "update"})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        af = self.add_files(
            form, "crm", "task"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        old = ClientTask.objects.filter(
            pk=self.object.pk
        ).first()  # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
        historyjson = {
            str(_("Задача")): "" if self.object.name == old.name else self.object.name,
            str(_("Статус")): ""
            if self.object.status.name == old.status.name
            else self.object.status.name,
            str(_("Начало")): ""
            if self.object.datebegin == old.datebegin
            else self.object.datebegin.strftime("%d.%m.%Y %H:%M"),
            str(_("Окончание")): ""
            if self.object.dateend == old.dateend
            else self.object.dateend.strftime("%d.%m.%Y %H:%M"),
            str(_("Тип в иерархии")): ""
            if self.object.structure_type.name == old.structure_type.name
            else self.object.structure_type.name,
            str(_("Тип")): ""
            if self.object.type.name == old.type.name
            else self.object.type.name,
            str(_("Стоимость")): ""
            if self.object.cost == old.cost
            else str(self.object.cost),
            str(_("Выполнен на, %")): ""
            if self.object.percentage == old.percentage
            else str(self.object.percentage),
            str(_("Инициатор")): ""
            if self.object.initiator.name == old.initiator.name
            else self.object.initiator.name,
            str(_("Исполнитель")): ""
            if self.object.assigner.username == old.assigner.username
            else self.object.assigner.username,
            str(_("Активность")): ""
            if self.object.is_active == old.is_active
            else "✓"
            if self.object.is_active
            else "-"
            # , str(_("Участники")):self.members.username
        }
        ModelLog.objects.create(
            componentname="cltsk",
            modelname="ClientTask",
            modelobjectid=self.object.id,
            author=self.object.author,
            log=json.dumps(historyjson),
        )
        return super().form_valid(form)


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienttaskcomments(request, taskid):
    currenttask = (
        ClientTask.objects.filter(id=taskid)
        .select_related(
            "client",
            "assigner",
            "structure_type",
            "type",
            "status",
            "author",
            "initiator",
        )
        .first()
    )
    currentuser = request.user.id
    if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id:
        obj_files_rights = 1
    else:
        obj_files_rights = 0

    taskcomment_costsum = ClientTaskComment.objects.filter(task=taskid).aggregate(
        Sum("cost")
    )
    taskcomment_timesum = ClientTaskComment.objects.filter(task=taskid).aggregate(
        Sum("time")
    )
    try:
        sec = taskcomment_timesum["time__sum"] * 3600
    except:
        sec = 0
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    seconds = sec
    taskcomment_list = ClientTaskComment.objects.filter(
        Q(author=request.user.id)
        | Q(
            task__client__members__in=[
                currentuser,
            ]
        ),
        is_active=True,
        task=taskid,
    )

    event_list = ClientEvent.objects.filter(task=currenttask, is_active=True)

    # print(taskcomment_list)
    button_taskcomment_create = ""
    # button_taskcomment_update = ''
    button_task_create = ""
    button_task_update = ""
    button_task_history = ""
    is_member = Client.objects.filter(
        members__in=[
            currentuser,
        ]
    ).exists()
    if (
        currentuser == currenttask.author_id
        or currentuser == currenttask.assigner_id
        or is_member
    ):
        button_task_create = button_taskcomment_create = button_event_create = _(
            "Добавить"
        )
        button_task_history = _("История")
        # button_taskcomment_create = "Добавить"
        # button_event_create = "Добавить"
        if (
            currentuser == currenttask.author_id
            or currentuser == currenttask.assigner_id
        ):
            button_task_update = _("Изменить")

    taskcomment_list = taskcomment_list.select_related("task", "author")
    event_list = event_list.select_related("client", "task", "type", "status")

    return render(
        request,
        "clienttask_detail.html",
        {
            "nodes": taskcomment_list.distinct().order_by(),
            # 'current_taskcomment': currenttaskcomment,
            "clienttask": currenttask,
            "obj_files_rights": obj_files_rights,
            "files": ClientFile.objects.filter(task=currenttask, is_active=True)
            .select_related("client", "task", "taskcomment", "event", "eventcomment")
            .order_by("uname"),
            "objtype": "clnttsk",
            "button_clienttask_create": button_task_create,
            "button_clienttask_update": button_task_update,
            "button_clienttask_history": button_task_history,
            # 'object_list': 'clienttask_list',
            "clienttaskcomment_costsum": taskcomment_costsum,
            "clienttaskcomment_timesum": taskcomment_timesum,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "button_clienttaskcomment_create": button_taskcomment_create,
            "enodes": event_list.distinct().order_by(),
            "button_event_create": button_event_create,
            "media_path": settings.MEDIA_URL,
        },
    )


class ClientTaskCommentDetail(DetailView):
    model = ClientTaskComment
    template_name = "taskcomment_detail.html"


class ClientTaskCommentCreate(AddFilesMixin, CreateView):
    model = ClientTaskComment
    form_class = ClientTaskCommentForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(ClientTaskCommentCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новый Комментарий")
        return context

    def form_valid(self, form):
        form.instance.task_id = self.kwargs["taskid"]
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новый коммент задачи клиента
        af = self.add_files(
            form, "crm", "taskcomment"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        return super(ClientTaskCommentCreate, self).form_valid(form)


class ClientTaskCommentUpdate(UpdateView):
    model = ClientTaskComment
    form_class = ClientTaskCommentForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(ClientTaskCommentUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Комментарий")
        context["files"] = ClientFile.objects.filter(
            taskcomment_id=self.kwargs["pk"], is_active=True
        ).order_by("uname")
        return context


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clientevents(request, clientid=0, pk=0):
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    evntstatus_selectid = 0
    try:
        evntstatus = request.POST["select_eventstatus"]
    except:
        event_list = ClientEvent.objects.filter(
            Q(author=request.user.id)
            | Q(assigner=request.user.id)
            | Q(
                client__members__in=[
                    currentuser,
                ]
            ),
            is_active=True,
            client=clientid,
            dateclose__isnull=True,
        )
    else:
        if evntstatus == "0":
            # если в выпадающем списке выбрано "Все активные"
            event_list = ClientEvent.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    client__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                client=clientid,
                dateclose__isnull=True,
            )
        else:
            if evntstatus == "-1":
                # если в выпадающем списке выбрано "Все"
                event_list = ClientEvent.objects.filter(
                    Q(author=request.user.id)
                    | Q(assigner=request.user.id)
                    | Q(
                        client__members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    client=clientid,
                )
            elif evntstatus == "-2":
                # если в выпадающем списке выбрано "Просроченные"
                event_list = ClientEvent.objects.filter(
                    Q(author=request.user.id)
                    | Q(assigner=request.user.id)
                    | Q(
                        client__members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    client=clientid,
                    dateclose__isnull=True,
                    dateend__lt=datetime.now(),
                )
            else:
                event_list = ClientEvent.objects.filter(
                    Q(author=request.user.id)
                    | Q(assigner=request.user.id)
                    | Q(
                        client__members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    client=clientid,
                    status=evntstatus,
                )  # , dateclose__isnull=True)
        evntstatus_selectid = evntstatus
    # *******************************

    # len_list = len(event_list)

    currentclient = Client.objects.get(id=clientid)

    obj_files_rights = 0

    if pk == 0:
        current_event = 0

    else:
        current_event = (
            ClientEvent.objects.filter(id=pk)
            .select_related("client", "task", "type", "status")
            .first()
        )
        if (
            currentuser == current_event.author_id
            or currentuser == current_event.assigner_id
        ):
            obj_files_rights = 1

    button_client_create = ""
    button_client_update = ""
    button_client_history = ""
    button_event_create = ""

    is_member = Client.objects.filter(
        members__in=[
            currentuser,
        ]
    ).exists()
    if (
        currentuser == currentclient.author_id
        or currentuser == currentclient.assigner_id
        or is_member
    ):
        button_client_create = button_event_create = _("Добавить")
        button_client_history = _("История")
        # button_event_create = "Добавить"
        if (
            currentuser == currentclient.author_id
            or currentuser == currentclient.assigner_id
        ):
            button_client_update = _("Изменить")

    event_list = event_list.select_related("client", "task", "type", "status")

    return render(
        request,
        "client_detail.html",
        {
            # .order_by('tree_id', 'level', '-dateend'),
            "nodes": event_list.distinct().order_by(),
            "current_event": current_event,
            "current_client": currentclient,
            "clientid": clientid,
            "user_companies": request.session["_auth_user_companies_id"],
            "obj_files_rights": obj_files_rights,
            "objtype": "clntevnt",
            "button_event_create": button_client_create,
            "buttonevent_update": button_client_update,
            "button_event_history": button_client_history,
            "eventstatus": Dict_ClientEventStatus.objects.filter(is_active=True),
            "eventtype": Dict_ClientEventType.objects.filter(is_active=True),
            "evntstatus_selectid": evntstatus_selectid,
            "object_list": "clientevent_list",
            # 'len_list': len_list,
        },
    )


class ClientEventCreate(AddFilesMixin, CreateView):
    model = ClientEvent
    form_class = ClientEventForm
    # template_name = 'event_create.html'
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.client_id = self.kwargs["clientid"]
        # print(self.kwargs['taskid'])
        if self.kwargs["taskid"] != 0:
            form.instance.task_id = self.kwargs["taskid"]
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новое событие клиента
        af = self.add_files(
            form, "crm", "event"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        self_task = ""
        self_task_id = 0
        self_task_name = ""
        if self.object.task:
            self_task = self.object.task
            self_task_id = self.object.task.id
            self_task_name = self.object.task.name
        self_status_name = ""
        if self.object.status:
            self_status_name = self.object.status.name
        self_type_name = ""
        if self.object.type:
            self_type_name = self.object.type.name
        historyjson = {
            str(_("Событие")): self.object.name,
            # _("Задача"): '#'+str(self_task_id)+'. '+self_task_name,
            str(_("Задача")): "#" + str(self_task_id) + ". " + self_task_name
            if self_task
            else "-",
            str(_("Статус")): self_status_name if self_status_name else "-",
            str(_("Начало")): self.object.datebegin.strftime("%d.%m.%Y %H:%M"),
            str(_("Окончание")): self.object.dateend.strftime("%d.%m.%Y %H:%M"),
            str(_("Тип")): self_type_name if self_type_name else "-",
            str(_("Место")): self.object.place if self.object.place else "-",
            str(_("Инициатор")): self.object.initiator.name,
            str(_("Исполнитель")): self.object.assigner.username,
            str(_("Активность")): "✓" if self.object.is_active else "-"
            # , str(_("Участники")):self.object.members.username
        }
        ModelLog.objects.create(
            componentname="clevnt",
            modelname="ClientEvent",
            modelobjectid=self.object.id,
            author=self.object.author,
            log=json.dumps(historyjson),
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClientEventCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новое Событие")
        return context

    def get_form_kwargs(self):
        kwargs = super(ClientEventCreate, self).get_form_kwargs()
        kwargs.update(
            {
                "user": self.request.user,
                "action": "create",
                "clientid": self.kwargs["clientid"],
                "taskid": self.kwargs["taskid"],
            }
        )
        return kwargs


class ClientEventUpdate(AddFilesMixin, UpdateView):
    model = ClientEvent
    form_class = ClientEventForm
    # template_name = 'task_update.html'
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(ClientEventUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Событие")
        context["files"] = ClientFile.objects.filter(
            event_id=self.kwargs["pk"], is_active=True
        ).order_by("uname")
        return context

    def get_form_kwargs(self):
        kwargs = super(ClientEventUpdate, self).get_form_kwargs()
        kwargs.update({"user": self.request.user, "action": "update"})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        af = self.add_files(
            form, "crm", "event"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        old = ClientEvent.objects.filter(
            pk=self.object.pk
        ).first()  # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
        # old_task_id = 0
        old_task = ""
        self_task = ""
        self_task_id = 0
        self_task_name = ""
        if old.task:
            old_task = old.task
            old_task_id = old.task.id
            # old_task_name = old.task.name
        if self.object.task:
            self_task = self.object.task
            self_task_id = self.object.task.id
            self_task_name = self.object.task.name
        historyjson = {
            str(_("Событие")): "" if self.object.name == old.name else self.name,
            str(_("Задача")): ""
            if self_task == old_task
            else ("#" + str(self_task_id) + ". " + self_task_name)
            if self_task
            else "-",
            str(_("Статус")): ""
            if self.object.status.name == old.status.name
            else self.object.status.name,
            str(_("Начало")): ""
            if self.object.datebegin == old.datebegin
            else self.object.datebegin.strftime("%d.%m.%Y %H:%M"),
            str(_("Окончание")): ""
            if self.object.dateend == old.dateend
            else self.object.dateend.strftime("%d.%m.%Y %H:%M"),
            str(_("Тип")): ""
            if self.object.type.name == old.type.name
            else self.object.type.name,
            str(_("Место")): ""
            if self.object.place == old.place
            else self.object.place,
            str(_("Инициатор")): ""
            if self.object.initiator.name == old.initiator.name
            else self.object.initiator.name,
            str(_("Исполнитель")): ""
            if self.object.assigner.username == old.assigner.username
            else self.object.assigner.username,
            str(_("Активность")): ""
            if self.object.is_active == old.is_active
            else "✓"
            if self.object.is_active
            else "-"
            # , str(_("Участники")):self.members.username
        }
        ModelLog.objects.create(
            componentname="clevnt",
            modelname="ClientEvent",
            modelobjectid=self.object.id,
            author=self.object.author,
            log=json.dumps(historyjson),
        )
        return super().form_valid(form)


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienteventcomments(request, eventid):
    currentevent = (
        ClientEvent.objects.filter(id=eventid)
        .select_related("client", "task", "type", "status")
        .first()
    )
    currentuser = request.user.id
    obj_files_rights = 0
    if currentuser == currentevent.author_id or currentuser == currentevent.assigner_id:
        obj_files_rights = 1

    eventcomment_list = ClientEventComment.objects.filter(
        Q(author=request.user.id)
        | Q(
            event__client__members__in=[
                currentuser,
            ]
        ),
        is_active=True,
        event=eventid,
    )
    # print(taskcomment_list)
    button_eventcomment_create = ""
    # button_eventcomment_update = ''
    button_event_create = ""
    button_event_update = ""
    button_event_history = ""
    is_member = Client.objects.filter(
        members__in=[
            currentuser,
        ]
    ).exists()
    if (
        currentuser == currentevent.author_id
        or currentuser == currentevent.assigner_id
        or is_member
    ):
        button_event_create = button_eventcomment_create = _("Добавить")
        button_event_history = _("История")
        # button_eventcomment_create = "Добавить"
        if (
            currentuser == currentevent.author_id
            or currentuser == currentevent.assigner_id
        ):
            button_event_update = _("Изменить")

    eventcomment_list = eventcomment_list.select_related("event", "author")

    return render(
        request,
        "clientevent_detail.html",
        {
            "nodes": eventcomment_list.distinct().order_by(),
            # 'current_eventcomment': currenteventcomment,
            "clientevent": currentevent,
            "obj_files_rights": obj_files_rights,
            "files": ClientFile.objects.filter(event=currentevent, is_active=True)
            .select_related("client", "task", "taskcomment", "event", "eventcomment")
            .order_by("uname"),
            "objtype": "clntevntcmnt",
            "button_clientevent_create": button_event_create,
            "button_clientevent_update": button_event_update,
            "button_clientevent_history": button_event_history,
            # 'object_list': 'clientevent_list',
            "button_clienteventcomment_create": button_eventcomment_create,
        },
    )


class ClientEventCommentDetail(DetailView):
    model = ClientEventComment
    template_name = "eventcomment_detail.html"


class ClientEventCommentCreate(AddFilesMixin, CreateView):
    model = ClientEventComment
    form_class = ClientEventCommentForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(ClientEventCommentCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новый Комментарий")
        return context

    def form_valid(self, form):
        form.instance.event_id = self.kwargs["eventid"]
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новый коммент события клиента
        af = self.add_files(
            form, "crm", "eventcomment"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        return super(ClientEventCommentCreate, self).form_valid(form)


class ClientEventCommentUpdate(UpdateView):
    model = ClientEventComment
    form_class = ClientEventCommentForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(ClientEventCommentUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Комментарий")
        context["files"] = ClientFile.objects.filter(
            eventcomment_id=self.kwargs["pk"], is_active=True
        ).order_by("uname")
        return context


### *** тестовый коммент *** ###
### *** второй тестовый коммент *** ###
"""
# *** ИСТОРИИ ИЗМЕНЕНИЯ СТАТУСОВ КЛИЕНТОВ И ЗАДАЧ ***

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienthistory(request, pk=0):

    #if companyid == 0:
    #   companyid = request.session['_auth_user_currentcompany_id']
    #current_company = Company.objects.get(id=companyid)

    if pk == 0:
       current_client = 0
    else:
       current_client = Client.objects.get(id=pk)

    comps = request.session['_auth_user_companies_id']

    nodes = ClientStatusLog.objects.filter(client_id=pk, is_active=True)
    table = ClientStatusLogTable(nodes)
    #nodes = ProjectStatusLog.objects.filter(project_id=pk, is_active=True)
    #table = ProjectStatusLogTable(nodes)
    
    RequestConfig(request).configure(table)

    return render(request, "client_history.html", {
                              'nodes': nodes, 
                              'current_client':current_client,
                              #'current_company':current_company,
                              #'companyid':companyid,
                              'user_companies': comps,
                              'table': table,                                                           
                                                })     

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienttaskhistory(request, pk=0):

    if pk == 0:
       current_task = 0
    else:
       current_task = ClientTask.objects.get(id=pk)

    comps = request.session['_auth_user_companies_id']

    nodes = ClientTaskStatusLog.objects.filter(task_id=pk, is_active=True)
    table = ClientTaskStatusLogTable(nodes)  

    RequestConfig(request).configure(table)      

    return render(request, "clienttask_history.html", {
                              'nodes': nodes, 
                              'current_task': current_task,
                              'user_companies': comps,  
                              'table': table,                                                               
                                                })

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienteventhistory(request, pk=0):

    if pk == 0:
       current_event = 0
    else:
       current_event = ClientEvent.objects.get(id=pk)

    comps = request.session['_auth_user_companies_id']

    nodes = ClientEventStatusLog.objects.filter(event_id=pk, is_active=True)
    table = ClientEventStatusLogTable(nodes)  

    RequestConfig(request).configure(table)      

    return render(request, "clientevent_history.html", {
                              'nodes': nodes, 
                              'current_event': current_event,
                              'user_companies': comps,  
                              'table': table,                                                               
                                                })
"""


# *** ФИЛЬТРЫ СПИСКОВ ***
@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clientfilter(request):
    # if request.user.is_authenticated():
    companyid = request.GET["companyid"]
    clntstatus = request.GET["clientstatus"]
    clnttype = request.GET["clienttype"]
    # _rights = request.GET['obj_files_rights']
    if companyid == 0:
        companyid = request.session["_auth_user_currentcompany_id"]
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    if clntstatus == "0":
        # если в выпадающем списке выбрано "Все активные"
        client_list = Client.objects.filter(
            Q(author=request.user.id)
            | Q(manager=request.user.id)
            | Q(
                members__in=[
                    currentuser,
                ]
            ),
            is_active=True,
            company=companyid,
            dateclose__isnull=True,
        )
    else:
        if clntstatus == "-1":
            # если в выпадающем списке выбрано "Все"
            client_list = Client.objects.filter(
                Q(author=request.user.id)
                | Q(manager=request.user.id)
                | Q(
                    members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                company=companyid,
            )
        elif clntstatus == "-2":
            # если в выпадающем списке выбрано "Просроченные"
            client_list = Client.objects.filter(
                Q(author=request.user.id)
                | Q(manager=request.user.id)
                | Q(
                    members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                company=companyid,
                dateclose__isnull=True,
                dateend__lt=datetime.now(),
            )
        else:
            client_list = Client.objects.filter(
                Q(author=request.user.id)
                | Q(manager=request.user.id)
                | Q(
                    members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                company=companyid,
                status=clntstatus,
            )
    # *******************************
    # **** фильтр по типу ***
    if clnttype != "-1":
        client_list = client_list.filter(Q(type=clnttype))
    # *** фильтр по принадлежности ***
    myclntuser = request.GET["myclientuser"]
    if myclntuser == "0":
        client_list = client_list.filter(
            Q(
                members__in=[
                    currentuser,
                ]
            )
        )
    elif myclntuser == "1":
        client_list = client_list.filter(Q(author=request.user.id))
    elif myclntuser == "2":
        client_list = client_list.filter(Q(manager=request.user.id))
    nodes = (
        client_list.select_related(
            "company",
            "manager",
            "user",
            "protocoltype",
            "type",
            "status",
            "currency",
            "initiator",
            "author",
        )
        .order_by()
        .distinct()
    )
    object_message = ""
    if len(nodes) == 0:
        object_message = _("Клиенты не найдены!")
    return render(
        request,
        "clients_list.html",
        {
            "nodes": nodes,
            "object_list": "client_list",
            "object_message": object_message,
        },
    )


# else:
#    return JsonResponse({'error': 'Only authenticated users'}, status=404)
# return render(request, 'clients_list.html', 'Информация недоступна')


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienttaskfilter(request):
    clientid = request.GET["clientid"]
    taskstatus = request.GET["taskstatus"]
    tasktype = request.GET["tasktype"]
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    # tskstatus_selectid = 0
    if taskstatus == "0":
        # если в выпадающем списке выбрано "Все активные"
        task_list = ClientTask.objects.filter(
            Q(author=request.user.id)
            | Q(assigner=request.user.id)
            | Q(
                client__members__in=[
                    currentuser,
                ]
            ),
            is_active=True,
            client=clientid,
            dateclose__isnull=True,
        )
    else:
        if taskstatus == "-1":
            # если в выпадающем списке выбрано "Все"
            task_list = ClientTask.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    client__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                client=clientid,
            )
        elif taskstatus == "-2":
            # если в выпадающем списке выбрано "Просроченные"
            task_list = ClientTask.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    client__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                client=clientid,
                dateclose__isnull=True,
                dateend__lt=datetime.now(),
            )
        else:
            task_list = ClientTask.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    client__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                client=clientid,
                status=taskstatus,
            )
    # *** фильтр по типу ***
    if tasktype != "-1":
        task_list = task_list.filter(Q(type=tasktype))
    # *** фильтр по принадлежности ***
    mytskuser = request.GET["mytaskuser"]
    if mytskuser == "0":
        task_list = task_list.filter(
            Q(
                client__members__in=[
                    currentuser,
                ]
            )
        )
    elif mytskuser == "1":
        task_list = task_list.filter(Q(author=request.user.id))
    elif mytskuser == "2":
        task_list = task_list.filter(Q(assigner=request.user.id))
    # *******************************
    nodes = (
        task_list.select_related(
            "client",
            "assigner",
            "structure_type",
            "type",
            "status",
            "author",
            "initiator",
        )
        .distinct()
        .order_by()
    )
    object_message = ""
    if len(nodes) == 0:
        object_message = _("Задачи не найдены!")
    return render(
        request,
        "objects_list.html",
        {
            "nodes": nodes,
            "object_list": "clienttask_list",
            "object_message": object_message,
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienteventfilter(request):
    clientid = request.GET["clientid"]
    eventstatus = request.GET["eventstatus"]
    eventtype = request.GET["eventtype"]
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    # tskstatus_selectid = 0
    # print('////////*******************************')
    # print(request)
    if eventstatus == "0":
        # если в выпадающем списке выбрано "Все активные"
        event_list = ClientEvent.objects.filter(
            Q(author=request.user.id)
            | Q(assigner=request.user.id)
            | Q(
                client__members__in=[
                    currentuser,
                ]
            ),
            is_active=True,
            client=clientid,
            dateclose__isnull=True,
        )
    else:
        if eventstatus == "-1":
            # если в выпадающем списке выбрано "Все"
            event_list = ClientEvent.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    client__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                client=clientid,
            )
        elif eventstatus == "-2":
            # если в выпадающем списке выбрано "Просроченные"
            event_list = ClientEvent.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    client__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                client=clientid,
                dateclose__isnull=True,
                dateend__lt=datetime.now(),
            )
        else:
            event_list = ClientEvent.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    client__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                client=clientid,
                status=eventstatus,
            )
    # *** фильтр по типу ***
    if eventtype != "-1":
        event_list = event_list.filter(Q(type=eventtype))
    # *** фильтр по принадлежности ***
    myevntuser = request.GET["myeventuser"]
    if myevntuser == "0":
        event_list = event_list.filter(
            Q(
                client__members__in=[
                    currentuser,
                ]
            )
        )
    elif myevntuser == "1":
        event_list = event_list.filter(Q(author=request.user.id))
    elif myevntuser == "2":
        event_list = event_list.filter(Q(assigner=request.user.id))
    # *******************************
    enodes = (
        event_list.select_related("client", "task", "type", "status")
        .distinct()
        .order_by()
    )
    # print(enodes)
    event_message = ""
    len_elist = len(enodes)
    if len_elist == 0:
        event_message = _("События не найдены!")
    return render(
        request,
        "clientevents_objects_list.html",
        {
            "enodes": enodes,
            "event_list": "clientevent_list",
            "event_message": event_message,
            "clientid": clientid,
        },
    )


# for Dashboard
def clients_tasks_events(request):
    currentuser = request.user.id
    companies_id = request.session["_auth_user_companies_id"]
    date_end = datetime.now() + timedelta(days=10)
    # print(request, date_end)

    clients_tasks_list = (
        ClientTask.objects.filter(
            Q(client__author=request.user.id)
            | Q(client__initiator=request.user.id)
            | Q(client__manager=request.user.id)
            | Q(author=request.user.id)
            | Q(initiator=request.user.id)
            | Q(assigner=request.user.id),
            is_active=True,
            status__is_close=False,
            client__company__in=companies_id,
            dateclose__isnull=True,
            dateend__lte=date_end,
        )
        .select_related(
            "client", "type", "type", "status", "initiator", "assigner", "author"
        )
        .order_by("dateend", "type")
        .distinct()
    )
    clients_events_list = (
        ClientEvent.objects.filter(
            Q(client__author=request.user.id)
            | Q(client__initiator=request.user.id)
            | Q(client__manager=request.user.id)
            | Q(task__author=request.user.id)
            | Q(task__initiator=request.user.id)
            | Q(task__assigner=request.user.id)
            | Q(author=request.user.id)
            | Q(initiator=request.user.id)
            | Q(assigner=request.user.id),
            is_active=True,
            status__is_close=False,
            dateclose__isnull=True,
            client__company__in=companies_id,
            dateend__lte=date_end,
        )
        .select_related(
            "client", "task", "type", "status", "initiator", "assigner", "author"
        )
        .order_by("dateend", "status")
        .distinct()
    )

    # print(projects_list, projects_tasks_list)

    return (clients_tasks_list, clients_events_list)
