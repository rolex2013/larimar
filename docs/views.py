from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from datetime import datetime, timedelta  # , date, time
import json
import requests
from django.db import connection

from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    DetailView,
)  # , View, TemplateView, ListView
from django.views.generic.edit import UpdateView  # , DeleteView

from django.db.models import Q  # , Count, Min, Max, Sum, Avg

from companies.models import Company
from .models import (
    Doc,
    DocVer,
    DocTask,
    DocTaskComment,
    Dict_DocType,
    Dict_DocStatus,
    Dict_DocTaskType,
    Dict_DocTaskStatus,
    DocVerFile,
)
from .forms import DocForm, DocTaskForm, DocTaskFormUpdate, DocTaskCommentForm  # , DocTaskUpdateForm

from main.models import ModelLog

from main.utils import AddFilesMixin

from django.utils.translation import gettext_lazy as _


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def docs(request, companyid=0, pk=0):
    if companyid == 0:
        companyid = request.session["_auth_user_currentcompany_id"]

    request.session["_auth_user_currentcomponent"] = "doc"

    # *** фильтруем по статусу ***
    currentuser = request.user.id
    docstatus_selectid = 0
    # mydocstatus = 0 # для фильтра "Мои документы"
    try:
        docstatus = request.POST["select_docstatus"]
    except:
        doc_list = Doc.objects.filter(
            Q(author=request.user.id)
            | Q(manager=request.user.id)
            | Q(
                members__in=[
                    currentuser,
                ]
            )
            | Q(docver_doc__is_public=True),
            is_active=True,
            company=companyid,
        )
    else:
        if docstatus == "0":
            # если в выпадающем списке выбрано "Все активные"
            doc_list = Doc.objects.filter(
                Q(author=request.user.id)
                | Q(manager=request.user.id)
                | Q(
                    members__in=[
                        currentuser,
                    ]
                )
                | Q(docver_doc__is_public=True),
                is_active=True,
                company=companyid,
            )
        else:
            if docstatus == "-1":
                # если в выпадающем списке выбрано "Все"
                doc_list = Doc.objects.filter(
                    Q(author=request.user.id)
                    | Q(manager=request.user.id)
                    | Q(
                        members__in=[
                            currentuser,
                        ]
                    )
                    | Q(docver_doc__is_public=True),
                    is_active=True,
                    company=companyid,
                )
            elif docstatus == "-2":
                # если в выпадающем списке выбрано "Просроченные"
                doc_list = Doc.objects.filter(
                    Q(author=request.user.id)
                    | Q(manager=request.user.id)
                    | Q(
                        members__in=[
                            currentuser,
                        ]
                    )
                    | Q(docver_doc__is_public=True),
                    is_active=True,
                    company=companyid,
                )
            else:
                doc_list = Doc.objects.filter(
                    Q(author=request.user.id)
                    | Q(manager=request.user.id)
                    | Q(
                        members__in=[
                            currentuser,
                        ]
                    )
                    | Q(docver_doc__is_public=True),
                    is_active=True,
                    company=companyid,
                    status=docstatus,
                )
        docstatus_selectid = docstatus

    len_list = len(doc_list)

    current_company = (
        Company.objects.filter(id=companyid)
        .select_related("author", "structure_type", "type", "currency")
        .first()
    )

    obj_files_rights = 0

    if pk == 0:
        current_doc = 0
    else:
        # current_doc = Doc.objects.get(id=pk)
        current_doc = (
            Doc.objects.filter(id=pk)
            .select_related("author", "company", "status", "type", "manager")
            .first()
        )
        if (
            currentuser == current_doc.author_id
            or currentuser == current_doc.manager_id
        ):
            obj_files_rights = 1

    button_company_select = ""
    button_company_create = ""
    button_company_update = ""
    button_doc_create = ""

    # здесь нужно условие для button_company_create
    # если текущий пользователь не является автором созданной текущей организации, то добавлять и изменять Компанию можно только в приложении Организации
    # button_company_create = _('Добавить')
    # здесь нужно условие для button_company_update
    # button_company_update = _('Изменить')
    # здесь нужно условие для button_doc_create
    # button_doc_create = _('Добавить')
    # здесь нужно условие для button_company_select
    comps = request.session["_auth_user_companies_id"]
    if len(comps) > 1:
        button_company_select = _("Сменить организацию")
    if currentuser == current_company.author_id:
        button_company_create = _("Добавить")
        button_company_update = _("Изменить")
        button_doc_create = _("Добавить")
    if current_company in comps:
        button_doc_create = _("Добавить")
    nodes = (
        doc_list.select_related("author", "company", "status", "type", "manager")
        .distinct()
        .order_by()
    )
    return render(
        request,
        "company_detail.html",
        {
            "nodes": nodes,
            "current_doc": current_doc,
            "current_company": current_company,
            "companyid": companyid,
            "user_companies": comps,
            "obj_files_rights": obj_files_rights,
            "button_company_select": button_company_select,
            "button_company_create": button_company_create,
            "button_company_update": button_company_update,
            "button_doc_create": button_doc_create,
            "docstatus": Dict_DocStatus.objects.filter(is_active=True),
            "doctype": Dict_DocType.objects.filter(is_active=True),
            "docstatus_selectid": docstatus_selectid,
            "object_list": "doc_list",
            "component_name": "docs",
            "len_list": len_list,
            # 'is_doc': True,
        },
    )


class DocCreate(AddFilesMixin, CreateView):
    model = Doc
    form_class = DocForm
    # template_name = 'doc_create.html'
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.company_id = self.kwargs["companyid"]
        # if self.kwargs['parentid'] != 0:
        #   form.instance.parent_id = self.kwargs['parentid']
        form.instance.author_id = self.request.user.id
        is_public = form.cleaned_data["is_public"]
        self.object = form.save()  # Созадём новый документ
        # Создаём первую версию Документа
        newdocver = DocVer.objects.create(
            doc_id=self.object.id,
            vernumber=1,
            name=self.object.name,
            description=self.object.description,
            datepublic=self.object.datepublic,
            is_public=is_public,
            is_actual=True,
            is_active=self.object.is_active,
            status=self.object.status,
            type=self.object.type,
            author=self.object.author,
            manager=self.object.manager,
        )
        af = self.add_files(
            form, "doc", "document"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        memb = self.object.members.values_list("id", "username").all()
        membersstr = ""
        for mem in memb:
            newdocver.members.add(mem[0])
            membersstr = membersstr + mem[1] + ","
        newdocver.save()
        # Делаем первую запись в историю изменений Документа (версии)
        historyjson = {
            str(_("Номер")): "1",
            str(_("Актуальн.")): newdocver.id,
            str(_("Наименование")): self.object.name,
            str(_("Тип")): self.object.type.name,
            str(_("Статус")): self.object.status.name,
            str(_("Менеджер")): self.object.manager.username,
            str(_("Участники")): membersstr,
            str(_("Активн.")): "✓" if self.object.is_active else "-",
        }
        ModelLog.objects.create(
            componentname="doc",
            modelname="Doc",
            modelobjectid=self.object.id,
            author=self.object.author,
            log=json.dumps(historyjson),
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Новый Документ")
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


class DocUpdate(AddFilesMixin, UpdateView):
    model = Doc
    form_class = DocForm
    # template_name = 'doc_update.html'
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Изменить Документ")
        doc = Doc.objects.filter(id=self.kwargs["pk"]).first()
        context["files"] = DocVerFile.objects.filter(
            doc_id=self.kwargs["pk"], docver_id=doc.docver, is_active=True
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
        old = Doc.objects.filter(
            pk=self.object.pk
        ).first()  # вместо objects.get(), чтоб не вызывало исключения при создании нового объекта
        oldfiles = DocVerFile.objects.filter(docver_id=old.docver, is_active=True)
        old_memb = old.members.values_list("id", "username").all()
        old_memb_count = old_memb.count()
        old_memb_list = list(old_memb)
        # print(oldfiles)
        # print(old_memb_list)
        is_public = form.cleaned_data["is_public"]
        self.object = form.save()  # записываем, чтобы посчитать номер версии
        vernumber = (
            DocVer.objects.filter(doc_id=self.object.id)
            .order_by("-vernumber")
            .values_list("vernumber")
            .first()
        )
        vernumber = int(vernumber[0]) + 1
        docver_unactual = DocVer.objects.filter(doc_id=self.object.id).update(
            is_actual=False
        )
        newdocver = DocVer.objects.create(
            doc_id=self.object.id,
            vernumber=vernumber,
            name=self.object.name,
            description=self.object.description,
            datepublic=self.object.datepublic,
            is_public=is_public,
            is_actual=True,
            is_active=self.object.is_active,
            status=self.object.status,
            type=self.object.type,
            author=self.object.author,
            manager=self.object.manager,
        )
        af = self.add_files(
            form, "doc", "document"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        # переносим все файлы из старой версии
        for f in oldfiles:
            newfiles = DocVerFile.objects.create(
                doc_id=self.object.id, docver_id=newdocver.id, is_active=True
            )
            # print('old:' + str(f.id) + f.name)
            newfiles.name = f.name
            newfiles.uname = f.uname
            newfiles.psize = f.psize
            newfiles.pfile = f.pfile
            newfiles.datecreate = f.datecreate
            newfiles.author_id = f.author_id
            newfiles.save()

        # записываем новых Участников
        memb = self.object.members.values_list("id", "username").all()
        memb_count = memb.count()
        is_members_changed = False
        if old_memb_count != memb_count:
            is_members_changed = True
        # print(list(memb))
        membersstr = ""
        for mem in memb:
            newdocver.members.add(mem[0])
            membersstr = membersstr + mem[1] + ","
            if is_members_changed is False:
                if old_memb_list.count(mem) == 0:
                    is_members_changed = True
        newdocver.save()
        historyjson = {
            str(_("Номер")): newdocver.vernumber,
            str(_("Актуальн.")): newdocver.id,
            str(_("Наименование")): ""
            if self.object.name == old.name
            else self.object.name,
            str(_("Тип")): ""
            if self.object.type.name == old.type.name
            else self.object.type.name,
            str(_("Статус")): ""
            if self.object.status.name == old.status.name
            else self.object.status.name,
            str(_("Менеджер")): ""
            if self.object.manager.username == old.manager.username
            else self.object.manager.username,
            # "Участники": '' if memb == old_memb else membersstr,
            str(_("Участники")): "" if is_members_changed is False else membersstr,
            str(_("Активн.")): ""
            if self.object.is_active == old.is_active
            else "✓"
            if self.object.is_active
            else "-",
        }
        ModelLog.objects.create(
            componentname="doc",
            modelname="Doc",
            modelobjectid=self.object.id,
            author=self.object.author,
            log=json.dumps(historyjson),
        )
        return super().form_valid(form)  # super(ProjectUpdate, self).form_valid(form)


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def doctasks(request, pk=0):
    currentuser = request.user.id
    # *** фильтруем по статусу ***
    tskstatus_selectid = 0
    doc = (
        Doc.objects.filter(id=pk)
        .select_related("author", "company", "status", "type", "manager")
        .first()
    )
    docverid = doc.docver

    try:
        tskstatus = request.POST["select_taskstatus"]
    except:
        task_list = DocTask.objects.filter(
            Q(author=request.user.id) | Q(assigner=request.user.id),
            is_active=True,
            docver=docverid,
            dateclose__isnull=True,
        )
    else:
        if tskstatus == "0":
            # если в выпадающем списке выбрано "Все активные"
            task_list = DocTask.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    doc__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                docver=docverid,
                dateclose__isnull=True,
            )
        else:
            if tskstatus == "-1":
                # если в выпадающем списке выбрано "Все"
                task_list = DocTask.objects.filter(
                    Q(author=request.user.id)
                    | Q(assigner=request.user.id)
                    | Q(
                        doc__members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    docver=docverid,
                )
            elif tskstatus == "-2":
                # если в выпадающем списке выбрано "Просроченные"
                task_list = DocTask.objects.filter(
                    Q(author=request.user.id)
                    | Q(assigner=request.user.id)
                    | Q(
                        doc__members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    docver=docverid,
                    dateclose__isnull=True,
                    dateend__lt=datetime.now(),
                )
            else:
                task_list = DocTask.objects.filter(
                    Q(author=request.user.id)
                    | Q(assigner=request.user.id)
                    | Q(
                        doc__members__in=[
                            currentuser,
                        ]
                    ),
                    is_active=True,
                    docver=docverid,
                    status=tskstatus,
                )  # , dateclose__isnull=True)
        tskstatus_selectid = tskstatus
    # *******************************
    currentdoc = doc  # Doc.objects.filter(id=pk).first()
    # currentdocver = DocVer.objects.filter(id=docverid).first()
    currentdocver = (
        DocVer.objects.filter(doc_id=pk, is_actual=True)
        .select_related("author", "doc", "status", "type", "manager")
        .first()
    )

    current_task = (
        DocTask.objects.filter(doc_id=pk, docver_id=docverid)
        .select_related("author", "doc", "docver", "assigner", "status", "type")
        .first()
    )

    button_doc_update = ""
    button_doc_history = ""
    button_task_create = ""

    obj_files_rights = 0
    if (
        currentuser == currentdoc.author_id
        or currentuser == currentdocver.author_id
        or currentuser == currentdocver.manager_id
    ):
        obj_files_rights = 1

    is_member = Doc.objects.filter(
        id=pk,
        members__in=[
            currentuser,
        ],
    ).exists()
    if (
        currentuser == currentdoc.author_id
        or currentuser == currentdocver.author_id
        or currentuser == currentdocver.manager_id
        or is_member
    ):
        button_doc_history = _("Версии")
        # Версия док-та создаётся всегда, но мало-ли... )))
        if currentdocver:
            # print(currentdocver)
            if currentdocver and currentdocver.is_public is False:
                button_task_create = _("Добавить")
            if (
                (
                    currentuser == currentdoc.author_id
                    or currentuser == currentdocver.author_id
                    or currentuser == currentdocver.manager_id
                )
                and currentdocver.is_public is False
                and currentdoc.doctask == 0
            ):
                button_doc_update = _("Изменить")

    task_list = task_list.select_related(
        "author", "doc", "docver", "assigner", "status", "type"
    )

    return render(
        request,
        "doc_detail.html",
        {
            "nodes": task_list.distinct().order_by(),  # .order_by('tree_id', 'level', '-dateend'),
            "current_task": current_task,
            "current_doc": currentdoc,
            "docid": currentdoc.id,
            "current_docver": currentdocver.vernumber,
            "docverid": docverid,
            "user_companies": request.session["_auth_user_companies_id"],
            "obj_files_rights": obj_files_rights,
            "files": DocVerFile.objects.filter(docver=currentdocver, is_active=True)
            .select_related("author", "doc", "docver", "task", "taskcomment")
            .order_by("uname"),
            "objtype": "doc",
            "is_member": is_member,
            "media_path": settings.MEDIA_URL,
            "button_doc_update": button_doc_update,
            "button_doc_history": button_doc_history,
            "button_task_create": button_task_create,
            # 'button_task_history': button_task_history,
            "taskstatus": Dict_DocTaskStatus.objects.filter(is_active=True),
            "tasktype": Dict_DocTaskType.objects.filter(is_active=True),
            "tskstatus_selectid": tskstatus_selectid,
            "object_list": "doctask_list",
        },
    )


class DocTaskCreate(AddFilesMixin, CreateView):
    model = DocTask
    form_class = DocTaskForm
    # template_name = 'task_create.html'
    # template_name = 'doctasks_list.html'
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.doc_id = self.kwargs["docid"]
        form.instance.docver_id = self.kwargs["docverid"]
        # if self.kwargs['parentid'] != 0:
        #   form.instance.parent_id = self.kwargs['parentid']
        form.instance.author_id = self.request.user.id
        # form.instance.comment = self.comment
        doc = Doc.objects.filter(id=form.instance.doc_id).first()
        form.instance.name = doc.name + ". " + str(form.cleaned_data["type"])
        # print(form.instance.name)
        comment = form.cleaned_data["comment"]
        self.object = form.save()  # Созадём новую задачу Документа
        af = self.add_files(
            form, "doc", "task"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        if comment != "":
            # создаём Комментарий к Задаче
            cmnt = DocTaskComment.objects.create(
                task_id=self.object.id,
                author_id=form.instance.author_id,
                description=comment,
            )
        historyjson = {
            str(_("Задача")): self.object.name,
            str(_("Статус")): self.object.status.name,
            # str(_("Начало")): self.object.datebegin.strftime('%d.%m.%Y %H:%M'),
            str(_("Окончание")): self.object.dateend.strftime("%d.%m.%Y"),
            # str(_("Тип в иерархии")): self.object.structure_type.name,
            str(_("Тип")): self.object.type.name,
            # str(_("Стоимость")): str(self.object.cost),
            # str(_("Выполнен на, %")): str(self.object.percentage),
            # str(_("Инициатор")): self.object.initiator.name,
            str(_("Исполнитель")): self.object.assigner.username,
            str(_("Активность")): "✓" if self.object.is_active else "-"
            # , str(_("Участники")):self.object.members.username
        }
        ModelLog.objects.create(
            componentname="dctsk",
            modelname="DocTask",
            modelobjectid=self.object.id,
            author=self.object.author,
            log=json.dumps(historyjson),
        )
        # return super().form_valid(form)
        self.object.save()
        taskid = self.object.id
        url = reverse("my_doc:doctaskcomments", kwargs={"taskid": taskid})
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super(DocTaskCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новая Задача")
        return context

    def get_form_kwargs(self):
        kwargs = super(DocTaskCreate, self).get_form_kwargs()
        kwargs.update(
            {
                "user": self.request.user,
                "action": "create",
                "docid": self.kwargs["docid"],
                "docverid": self.kwargs["docverid"],
            }
        )
        # kwargs.update({'user': self.request.user, 'action': 'create', 'docid': self.kwargs['docid']})
        return kwargs


class DocTaskUpdate(AddFilesMixin, UpdateView):
    model = DocTask
    form_class = DocTaskFormUpdate
    # template_name = 'task_update.html'
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(DocTaskUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Задачу")
        context["files"] = DocVerFile.objects.filter(
            task_id=self.kwargs["pk"], is_active=True
        ).order_by("uname")
        return context

    def get_form_kwargs(self):
        kwargs = super(DocTaskUpdate, self).get_form_kwargs()
        kwargs.update({"user": self.request.user, "action": "update"})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        af = self.add_files(
            form, "doc", "task"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        old = DocTask.objects.filter(
            pk=self.object.pk
        ).first()  # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
        historyjson = {
            str(_("Задача")): "" if self.object.name == old.name else self.object.name,
            str(_("Статус")): ""
            if self.object.status.name == old.status.name
            else self.object.status.name,
            # str(_("Начало":'' if self.object.datebegin == old.datebegin else self.object.datebegin.strftime('%d.%m.%Y %H:%M'),
            str(_("Окончание")): ""
            if self.object.dateend == old.dateend
            else self.object.dateend.strftime("%d.%m.%Y %H:%M"),
            # str(_("Тип в иерархии")):'' if self.object.structure_type.name == old.structure_type.name else self.object.structure_type.name,
            str(_("Тип")): ""
            if self.object.type.name == old.type.name
            else self.object.type.name,
            # str(_("Стоимость":'' if self.object.cost == old.cost else str(self.object.cost),
            # str(_("Выполнен на, %":'' if self.object.percentage == old.percentage else str(self.object.percentage),
            # str(_("Инициатор":'' if self.object.initiator.name == old.initiator.name else self.object.initiator.name,
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
            componentname="dctsk",
            modelname="DocTask",
            modelobjectid=self.object.id,
            author=self.object.author,
            log=json.dumps(historyjson),
        )
        # return super().form_valid(form)
        self.object.save()
        taskid = self.object.id
        url = reverse("my_doc:doctaskcomments", kwargs={"taskid": taskid})
        return HttpResponseRedirect(url)


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def doctaskcomments(request, taskid):
    currenttask = DocTask.objects.filter(id=taskid).first()
    currentuser = request.user.id

    taskcomment_list = DocTaskComment.objects.filter(
        Q(author=request.user.id)
        | Q(
            task__doc__members__in=[
                currentuser,
            ]
        ),
        is_active=True,
        task=taskid,
    )

    button_taskcomment_create = ""
    # button_taskcomment_update = ''
    button_task_create = ""
    button_task_update = ""
    button_task_history = ""
    is_member = Doc.objects.filter(
        members__in=[
            currentuser,
        ]
    ).exists()
    obj_files_rights = 0
    if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id:
        obj_files_rights = 1
    if (
        currentuser == currenttask.author_id
        or currentuser == currenttask.assigner_id
        or is_member
    ):
        # button_task_create = 'Добавить'
        button_task_history = _("История")
        button_taskcomment_create = _("Добавить")
        if (
            currentuser == currenttask.author_id
            or currentuser == currenttask.assigner_id
        ):
            button_task_update = _("Изменить")

    taskcomment_list = taskcomment_list.select_related("author", "task")

    return render(
        request,
        "doctask_detail.html",
        {
            "nodes": taskcomment_list.distinct().order_by(),
            # 'node_files': n_files,
            # 'current_taskcomment': currenttaskcomment,
            "task": currenttask,
            "obj_files_rights": obj_files_rights,
            "files": DocVerFile.objects.filter(task=currenttask, is_active=True)
            .select_related("author", "doc", "docver", "task", "taskcomment")
            .order_by("uname"),
            "objtype": "doctsk",
            "media_path": settings.MEDIA_URL,
            #'button_task_create': button_task_create,
            "button_task_update": button_task_update,
            "button_task_history": button_task_history,
            "button_taskcomment_create": button_taskcomment_create,
        },
    )


class DocTaskCommentDetail(DetailView):
    model = DocTaskComment
    template_name = "doctaskcomment_detail.html"


class DocTaskCommentCreate(AddFilesMixin, CreateView):
    model = DocTaskComment
    form_class = DocTaskCommentForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Новый Комментарий")
        return context

    def form_valid(self, form):
        form.instance.task_id = self.kwargs["taskid"]
        form.instance.author_id = self.request.user.id
        self.object = form.save()
        af = self.add_files(
            form, "doc", "taskcomment"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        return super().form_valid(form)


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def docfilter(request):
    companyid = request.GET["companyid"]
    docstatus = request.GET["docstatus"]
    doctype = request.GET["doctype"]
    # currentdoc = Doc.objects.filter(id=docid).first()
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    # tskstatus_selectid = 0
    if docstatus == "0":
        # если в выпадающем списке выбрано "Все активные"
        doc_list = Doc.objects.filter(
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
        if docstatus == "-1":
            # если в выпадающем списке выбрано "Все"
            doc_list = Doc.objects.filter(
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
        # elif docstatus == "-2":
        # если в выпадающем списке выбрано "Просроченные"
        # date_format = '%Y-%m-%d'
        # today = datetime.datetime.now()
        # yesterday = today - timedelta(days=1)
        #   doc_list = DocTask.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, doc=docid, dateclose__isnull=True, dateend__lt=today)
        #   print(today)
        else:
            doc_list = Doc.objects.filter(
                Q(author=request.user.id)
                | Q(manager=request.user.id)
                | Q(
                    members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                company=companyid,
                status=docstatus,
            )
    # *** фильтр по типу ***
    if doctype != "-1":
        doc_list = doc_list.filter(Q(type=doctype))
    # *** фильтр по принадлежности ***
    mydocuser = request.GET["mydocuser"]
    if mydocuser == "0":
        doc_list = doc_list.filter(
            Q(
                doc__members__in=[
                    currentuser,
                ]
            )
        )
    elif mydocuser == "1":
        doc_list = doc_list.filter(Q(manager=request.user.id))
    elif mydocuser == "2":
        doc_list = doc_list.filter(Q(author=request.user.id))
    # *******************************
    nodes = (
        doc_list.select_related("author", "company", "status", "type", "manager")
        .distinct()
        .order_by()
    )
    object_message = ""
    if len(nodes) == 0:
        object_message = _("Задачи не найдены!")
    return render(
        request,
        "docs_list.html",
        {"nodes": nodes, "object_list": "doc_list", "object_message": object_message},
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def doctaskfilter(request):
    docid = request.GET["docid"]
    taskstatus = request.GET["taskstatus"]
    tasktype = request.GET["tasktype"]
    currentdoc = (
        Doc.objects.filter(id=docid)
        .select_related("author", "company", "status", "type", "manager")
        .first()
    )
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    # tskstatus_selectid = 0
    if taskstatus == "0":
        # если в выпадающем списке выбрано "Все активные"
        task_list = DocTask.objects.filter(
            Q(author=request.user.id)
            | Q(assigner=request.user.id)
            | Q(
                doc__members__in=[
                    currentuser,
                ]
            ),
            is_active=True,
            doc=docid,
            dateclose__isnull=True,
        )
    else:
        if taskstatus == "-1":
            # если в выпадающем списке выбрано "Все"
            task_list = DocTask.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    doc__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                doc=docid,
            )
        elif taskstatus == "-2":
            # если в выпадающем списке выбрано "Просроченные"
            # date_format = '%Y-%m-%d'
            today = datetime.now()
            # yesterday = today - timedelta(days=1)
            task_list = DocTask.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    doc__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                doc=docid,
                dateclose__isnull=True,
                dateend__lt=today,
            )
            print(today)
        else:
            task_list = DocTask.objects.filter(
                Q(author=request.user.id)
                | Q(assigner=request.user.id)
                | Q(
                    doc__members__in=[
                        currentuser,
                    ]
                ),
                is_active=True,
                doc=docid,
                status=taskstatus,
            )
    # *** фильтр по типу ***
    if tasktype != "-1":
        task_list = task_list.filter(Q(type=tasktype))
    # *** фильтр по принадлежности ***
    # mytskuser = request.GET['mytaskuser']
    # if mytskuser == "0":
    #   task_list = task_list.filter(Q(doc__members__in=[currentuser,]))
    # elif mytskuser == "1":
    #   task_list = task_list.filter(Q(author=request.user.id))
    # elif mytskuser == "2":
    #   task_list = task_list.filter(Q(assigner=request.user.id))
    # *******************************
    nodes = (
        task_list.select_related(
            "author", "doc", "docver", "assigner", "status", "type"
        )
        .distinct()
        .order_by()
    )
    object_message = ""
    if len(nodes) == 0:
        object_message = _("Задачи не найдены!")
    return render(
        request,
        "doctasks_list.html",
        {
            "nodes": nodes,
            "object_list": "doctask_list",
            "current_doc": currentdoc,
            "object_message": object_message,
        },
    )


def docver_change(request):
    docverid = request.GET["docverid"]
    if docverid == 0:
        return False
    # позиционируемся на нужной версии
    docver = (
        DocVer.objects.filter(id=docverid)
        .select_related("author", "doc", "status", "type", "manager")
        .first()
    )
    # делаем все версии Документа неактуальными
    DocVer.objects.filter(doc_id=docver.doc_id).update(is_actual=False)
    # делаем текущую версию Документа актуальной
    docver.is_actual = True
    docver.save()
    nodes = ModelLog.objects.filter(
        componentname="doc", modelobjectid=docver.doc_id, is_active=True
    )
    i = -1
    mas = []
    for node in nodes:
        i += 1
        mas.append(json.loads(node.log).items())
    current_object = (
        Doc.objects.filter(id=docver.doc_id)
        .select_related("author", "company", "status", "type", "manager")
        .first()
    )
    comps = request.session["_auth_user_companies_id"]
    return render(
        request,
        "object_history.html",
        {
            "nodes": nodes,
            "mas": mas,
            "current_object": current_object,
            "user_companies": comps,
            "objtype": "doc",
        },
    )


# for Dashboard
def docs_tasks(request):
    currentuser = request.user.id
    companies_id = request.session["_auth_user_companies_id"]
    date_end = datetime.now() + timedelta(days=10)
    # print(request, date_end)

    docs_tasks_list = (
        DocTask.objects.filter(
            Q(author=request.user.id)
            | Q(assigner=request.user.id)
            | Q(
                doc__members__in=[
                    currentuser,
                ]
            ),
            docver__doc__company__in=companies_id,
            is_active=True,
            dateclose__isnull=True,
            dateend__lte=date_end,
        )
        .select_related("doc", "docver", "type", "status", "assigner", "author")
        .order_by("dateend", "type")
        .distinct()
    )

    # print(projects_list, projects_tasks_list)

    return docs_tasks_list
