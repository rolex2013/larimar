from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, date, time
#import json
import requests
from django.db import connection

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView #, View, TemplateView, ListView
from django.views.generic.edit import UpdateView #, DeleteView

from django.db.models import Q #, Count, Min, Max, Sum, Avg

from companies.models import Company
from . models import Doc, DocVer, DocTask, DocTaskComment, Dict_DocType, Dict_DocStatus, Dict_DocTaskType, Dict_DocTaskStatus, DocFile
from .forms import DocForm

from main.utils import AddFilesMixin


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def docs(request, companyid=0, pk=0):

    if companyid == 0:
       companyid = request.session['_auth_user_currentcompany_id']

    request.session['_auth_user_currentcomponent'] = 'doc'

    # *** фильтруем по статусу ***
    currentuser = request.user.id
    docstatus_selectid = 0
    #mydocstatus = 0 # для фильтра "Мои документы"
    try:
       docstatus = request.POST['select_docstatus']
    except:
       doc_list = Doc.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid)
    else:
       if docstatus == "0":
          # если в выпадающем списке выбрано "Все активные"
          doc_list = Doc.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid)
       else:
          if docstatus == "-1":
             # если в выпадающем списке выбрано "Все"
             doc_list = Doc.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid)
          elif docstatus == "-2":
             # если в выпадающем списке выбрано "Просроченные"
             doc_list = Doc.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid)
          else:
             doc_list = Doc.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, status=docstatus)
       docstatus_selectid = docstatus
    #docstatus_myselectid = mydocstatus
    # *******************************
    #doc_list = doc_list.order_by('datepublic')
    #print(doc_list)
    len_list = len(doc_list)

    current_company = Company.objects.get(id=companyid)

    if pk == 0:
       current_doc = 0
    else:
       current_doc = Doc.objects.get(id=pk)

    button_company_select = ''
    button_company_create = ''
    button_company_update = ''
    button_doc_create = ''

    # здесь нужно условие для button_company_create
    # если текущий пользователь не является автором созданной текущей организации, то добавлять и изменять Компанию можно только в приложении Организации
    #button_company_create = 'Добавить'
    # здесь нужно условие для button_company_update
    #button_company_update = 'Изменить'
    # здесь нужно условие для button_doc_create
    #button_doc_create = 'Добавить'
    # здесь нужно условие для button_company_select
    comps = request.session['_auth_user_companies_id']
    if len(comps) > 1:
       button_company_select = 'Сменить организацию'
    if currentuser == current_company.author_id:
       button_company_create = 'Добавить'
       button_company_update = 'Изменить'
       button_doc_create = 'Добавить'
    if current_company in comps:
       button_doc_create = 'Добавить'
    nodes = doc_list.distinct().order_by()
    return render(request, "company_detail.html", {
                              'nodes': nodes,
                              'current_doc': current_doc,
                              'current_company': current_company,
                              'companyid': companyid,
                              'user_companies': comps,
                              'button_company_select': button_company_select,
                              'button_company_create': button_company_create,
                              'button_company_update': button_company_update,
                              'button_doc_create': button_doc_create,
                              'docstatus': Dict_DocStatus.objects.filter(is_active=True),
                              'doctype': Dict_DocType.objects.filter(is_active=True),
                              'docstatus_selectid': docstatus_selectid,
                              'object_list': 'doc_list',
                              'component_name': 'docs',
                              'len_list': len_list,
                                                })

class DocCreate(AddFilesMixin, CreateView):
    model = Doc
    form_class = DocForm
    #template_name = 'doc_create.html'
    template_name = 'object_form.html'

    def form_valid(self, form):
       form.instance.company_id = self.kwargs['companyid']
       #if self.kwargs['parentid'] != 0:
       #   form.instance.parent_id = self.kwargs['parentid']
       form.instance.author_id = self.request.user.id
       self.object = form.save() # Созадём новый документ
       af = self.add_files(form, 'doc', 'document') # добавляем файлы из формы (метод из AddFilesMixin)
       # Делаем первую запись в историю изменений проекта
       self_user_username = ''
       if self.object.user:
          self_user_username = self.user.username
       historyjson = {"Наименование": self.object.name,
                      "Тип": self.object.type.name,
                      "Статус": self.object.status.name,
                      "Менеджер": self.object.manager.username,
                      "Активн.": '✓' if self.object.is_active else '-'
                     }
       ModelLog.objects.create(componentname='doc', modelname="Doc", modelobjectid=self.object.id, author=self.object.author, log=json.dumps(historyjson))
       return super().form_valid(form)

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['header'] = 'Новый Документ'
       return context

    def get_form_kwargs(self):
       kwargs = super().get_form_kwargs()
       # здесь нужно условие для 'action': 'create'
       kwargs.update({'user': self.request.user, 'action': 'create', 'companyid': self.kwargs['companyid']})
       return kwargs

class DocUpdate(AddFilesMixin, UpdateView):
    model = Doc
    form_class = DocForm
    #template_name = 'doc_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['header'] = 'Изменить Документ'
       context['files'] = DocFile.objects.filter(doc_id=self.kwargs['pk'], is_active=True).order_by('uname')
       return context

    def get_form_kwargs(self):
       kwargs = super().get_form_kwargs()
       # здесь нужно условие для 'action': 'update'
       kwargs.update({'user': self.request.user, 'action': 'update'})
       return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False) # без commit=False происходит вызов save() Модели
        af = self.add_files(form, 'doc', 'document') # добавляем файлы из формы (метод из AddFilesMixin)
        old = Doc.objects.filter(pk=self.object.pk).first() # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
        old_user_username = ''
        self_user_username = ''
        if old.user:
           old_user_username = old.user.username
        if self.object.user:
           self_user_username = self.object.user.username
        historyjson = {"Наименование":'' if self.object.name == old.name else self.object.name,
                       "Тип":'' if self.object.type.name == old.type.name else self.object.type.name,
                       "Статус":'' if self.object.status.name == old.status.name else self.object.status.name,
                       "Менеджер":'' if self.object.manager.username == old.manager.username else self.object.manager.username,
                       "Активн.":'' if self.object.is_active == old.is_active else '✓' if self.object.is_active else '-'
                      }
        ModelLog.objects.create(componentname='doc', modelname="Doc", modelobjectid=self.object.id, author=self.object.author, log=json.dumps(historyjson))
        return super().form_valid(form) #super(ProjectUpdate, self).form_valid(form)


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def doctasks(request, docverid=0, pk=0):
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    tskstatus_selectid = 0
    try:
        tskstatus = request.POST['select_taskstatus']
    except:
        task_list = DocTask.objects.filter(
            Q(author=request.user.id) | Q(assigner=request.user.id) | Q(doc__members__in=[currentuser, ]),
            is_active=True, docver=docverid, dateclose__isnull=True)
    else:
        if tskstatus == "0":
            # если в выпадающем списке выбрано "Все активные"
            task_list = DocTask.objects.filter(
                Q(author=request.user.id) | Q(assigner=request.user.id) | Q(doc__members__in=[currentuser, ]),
                is_active=True, docver=docverid, dateclose__isnull=True)
        else:
            if tskstatus == "-1":
                # если в выпадающем списке выбрано "Все"
                task_list = DocTask.objects.filter(
                    Q(author=request.user.id) | Q(assigner=request.user.id) | Q(doc__members__in=[currentuser, ]),
                    is_active=True, docver=docverid)
            elif tskstatus == "-2":
                # если в выпадающем списке выбрано "Просроченные"
                task_list = DocTask.objects.filter(
                    Q(author=request.user.id) | Q(assigner=request.user.id) | Q(doc__members__in=[currentuser, ]),
                    is_active=True, docver=docverid, dateclose__isnull=True, dateend__lt=datetime.now())
            else:
                task_list = DocTask.objects.filter(
                    Q(author=request.user.id) | Q(assigner=request.user.id) | Q(doc__members__in=[currentuser, ]),
                    is_active=True, docver=docverid, status=tskstatus)  # , dateclose__isnull=True)
        tskstatus_selectid = tskstatus
    # *******************************

    #event_list = ClientEvent.objects.filter(client=clientid, is_active=True)
    ## len_elist = len(event_list)

    currentdocver = DocVer.objects.get(id=docverid)

    #taskcomment_costsum = DocTaskComment.objects.filter(task__docver_id=currentdocver.id).aggregate(Sum('cost'))
    #taskcomment_timesum = DocTaskComment.objects.filter(task__docver_id=currentdocver.id).aggregate(Sum('time'))
    #try:
    #    sec = taskcomment_timesum["time__sum"] * 3600
    #except:
    #    sec = 0
    #hours, sec = divmod(sec, 3600)
    #minutes, sec = divmod(sec, 60)
    #seconds = sec

    if pk == 0:
        current_task = 0
        #tree_task_id = 0
        #root_task_id = 0
        #tree_task_id = 0
    else:
        current_task = DocTask.objects.get(id=pk)
        #tree_task_id = current_task.tree_id
        #root_task_id = current_task.get_root().id
        #tree_task_id = current_task.tree_id

    #button_doc_create = ''
    button_doc_update = ''
    button_doc_history = ''
    button_task_create = ''

    is_member = Doc.objects.filter(members__in=[currentuser, ]).exists()
    if currentuser == currentdocver.author_id or currentuser == currentdocver.assigner_id or is_member:
        # button_client_create = 'Добавить'
        button_doc_history = 'История'
        button_task_create = 'Добавить'
        #button_event_create = 'Добавить'
        if currentuser == currentdocver.author_id or currentuser == currentdocver.assigner_id:
            button_doc_update = 'Изменить'

    return render(request, "doc_detail.html", {
        'nodes': task_list.distinct().order_by(),  # .order_by('tree_id', 'level', '-dateend'),
        'current_task': current_task,
        #'root_task_id': root_task_id,
        #'tree_task_id': tree_task_id,
        'current_docver': currentdocver,
        'docverid': docverid,
        'user_companies': request.session['_auth_user_companies_id'],
        'files': DocFile.objects.filter(docver=currentdocver, is_active=True).order_by('uname'),
        'objtype': 'doc',
        'media_path': settings.MEDIA_URL,
        #'button_client_create': button_client_create,
        'button_doc_update': button_doc_update,
        'button_doc_history': button_doc_history,
        'button_task_create': button_task_create,
        # 'button_task_history': button_task_history,
        #'taskstatus': Dict_DocTaskStatus.objects.filter(is_active=True),
        #'tasktype': Dict_DocTaskType.objects.filter(is_active=True),
        'tskstatus_selectid': tskstatus_selectid,
        'object_list': 'doctask_list',
        #'taskcomment_costsum': taskcomment_costsum,
        #'taskcomment_timesum': taskcomment_timesum,
        #'hours': hours, 'minutes': minutes, 'seconds': seconds,
        ## 'len_list': len_list,
        #'enodes': event_list.distinct().order_by(),
        ## 'len_elist': len_elist,
        #'button_event_create': button_event_create,
        #'eventstatus': Dict_ClientEventStatus.objects.filter(is_active=True),
        #'eventtype': Dict_ClientEventType.objects.filter(is_active=True),
        ## 'evntstatus_selectid': evntstatus_selectid,

    })

def doc_list(request):
    return render(request, "docdoc_list.html", {'nodes': nodes,})

def file_list(request):
    return render(request, "docfile_list.html", {'nodes': nodes,})

