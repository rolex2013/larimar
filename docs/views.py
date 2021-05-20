from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, date, time
import json
import requests
from django.db import connection

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView #, View, TemplateView, ListView
from django.views.generic.edit import UpdateView #, DeleteView

from django.db.models import Q #, Count, Min, Max, Sum, Avg

from companies.models import Company
from . models import Doc, DocVer, DocTask, DocTaskComment, Dict_DocType, Dict_DocStatus, Dict_DocTaskType, Dict_DocTaskStatus, DocVerFile
from .forms import DocForm, DocTaskForm #,DocTaskCommentForm

from main.models import ModelLog

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
                              #'is_doc': True,
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
       # Создаём первую версию Документа
       newdocver = DocVer.objects.create(doc_id=self.object.id, vernumber=1, name=self.object.name, description=self.object.description,
                                         datepublic=self.object.datepublic, is_actual=True, is_active=self.object.is_active,
                                         status=self.object.status, type=self.object.type, author=self.object.author,
                                         manager=self.object.manager)
       af = self.add_files(form, 'doc', 'document') # добавляем файлы из формы (метод из AddFilesMixin)
       memb = self.object.members.values_list('id', 'username').all()
       membersstr = ''
       for mem in memb:
           newdocver.members.add(mem[0])
           membersstr = membersstr + mem[1] + ','
       newdocver.save()
       # Делаем первую запись в историю изменений Документа
       historyjson = {"Номер": '1',
                      "Актуальн.": newdocver.id,
                      "Наименование": self.object.name,
                      "Тип": self.object.type.name,
                      "Статус": self.object.status.name,
                      "Менеджер": self.object.manager.username,
                      "Участники": membersstr,
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
       doc = Doc.objects.filter(id=self.kwargs['pk']).first()
       context['files'] = DocVerFile.objects.filter(doc_id=self.kwargs['pk'], docver_id=doc.docver, is_active=True).order_by('uname')
       return context

    def get_form_kwargs(self):
       kwargs = super().get_form_kwargs()
       # здесь нужно условие для 'action': 'update'
       kwargs.update({'user': self.request.user, 'action': 'update'})
       return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False) # без commit=False происходит вызов save() Модели
        old = Doc.objects.filter(pk=self.object.pk).first() # вместо objects.get(), чтоб не вызывало исключения при создании нового объекта
        oldfiles = DocVerFile.objects.filter(docver_id=old.docver, is_active=True)
        old_memb = old.members.values_list('id', 'username').all()
        old_memb_count = old_memb.count()
        old_memb_list = list(old_memb)
        #print(oldfiles)
        #print(old_memb_list)
        self.object = form.save() # записываем, чтобы посчитать номер версии
        vernumber = DocVer.objects.filter(doc_id=self.object.id).order_by('-vernumber').values_list('vernumber').first()
        vernumber = int(vernumber[0]) + 1
        docver_unactual = DocVer.objects.filter(doc_id=self.object.id).update(is_actual=False)
        newdocver = DocVer.objects.create(doc_id=self.object.id, vernumber=vernumber, name=self.object.name, description=self.object.description,
                                          datepublic=self.object.datepublic, is_actual=True, is_active=self.object.is_active,
                                          status=self.object.status, type=self.object.type, author=self.object.author,
                                          manager=self.object.manager)
        af = self.add_files(form, 'doc', 'document')  # добавляем файлы из формы (метод из AddFilesMixin)
        # переносим все файлы из старой версии
        for f in oldfiles:
            newfiles = DocVerFile.objects.create(doc_id=self.object.id, docver_id=newdocver.id, is_active=True)
            #print('old:' + str(f.id) + f.name)
            newfiles.name = f.name
            newfiles.uname = f.uname
            newfiles.psize = f.psize
            newfiles.pfile = f.pfile
            newfiles.datecreate = f.datecreate
            newfiles.author_id = f.author_id
            newfiles.save()

        # записываем новых Участников
        memb = self.object.members.values_list('id', 'username').all()
        memb_count = memb.count()
        is_members_changed = False
        if old_memb_count != memb_count:
            is_members_changed = True
        #print(list(memb))
        membersstr = ''
        for mem in memb:
            newdocver.members.add(mem[0])
            membersstr = membersstr + mem[1] + ','
            if is_members_changed == False:
                if old_memb_list.count(mem) == 0:
                    is_members_changed = True
        newdocver.save()
        historyjson = {"Номер": newdocver.vernumber,
                       "Актуальн.": newdocver.id,
                       "Наименование":'' if self.object.name == old.name else self.object.name,
                       "Тип":'' if self.object.type.name == old.type.name else self.object.type.name,
                       "Статус":'' if self.object.status.name == old.status.name else self.object.status.name,
                       "Менеджер":'' if self.object.manager.username == old.manager.username else self.object.manager.username,
                       #"Участники": '' if memb == old_memb else membersstr,
                       "Участники": '' if is_members_changed == False else membersstr,
                       "Активн.":'' if self.object.is_active == old.is_active else '✓' if self.object.is_active else '-'
                      }
        ModelLog.objects.create(componentname='doc', modelname="Doc", modelobjectid=self.object.id, author=self.object.author, log=json.dumps(historyjson))
        return super().form_valid(form) #super(ProjectUpdate, self).form_valid(form)


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def doctasks(request, pk=0):
    #print('======================')
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    tskstatus_selectid = 0
    doc = Doc.objects.filter(id=pk).first()
    docverid = doc.docver

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

    currentdoc = Doc.objects.filter(id=pk).first()
    #currentdocver = DocVer.objects.filter(id=docverid).first()
    currentdocver = DocVer.objects.filter(doc_id=pk, is_actual=True).first()
    #print(pk)

    #try:
    #    current_task = DocTask.objects.get(doc_id=pk, docver_id=docverid)
    #except DocTask.DoesNotExist:
    #    current_task = None
    # вместо этой конструкции можно писать короче:
    current_task = DocTask.objects.filter(doc_id=pk, docver_id=docverid).first()

    button_doc_update = ''
    button_doc_history = ''
    button_task_create = ''

    is_member = Doc.objects.filter(members__in=[currentuser, ]).exists()
    if currentuser == currentdocver.author_id or currentuser == currentdocver.assigner_id or is_member:
        button_doc_history = 'История'
        button_task_create = 'Добавить'
        if currentuser == currentdocver.author_id or currentuser == currentdocver.assigner_id:
            button_doc_update = 'Изменить'

    return render(request, "doc_detail.html", {
        'nodes': task_list.distinct().order_by(),  # .order_by('tree_id', 'level', '-dateend'),
        'current_task': current_task,
        'current_doc': currentdoc,
        'current_docver': currentdocver.vernumber,
        'docverid': docverid,
        'user_companies': request.session['_auth_user_companies_id'],
        'files': DocVerFile.objects.filter(docver=currentdocver, is_active=True).order_by('uname'),
        'objtype': 'doc',
        'media_path': settings.MEDIA_URL,
        'button_doc_update': button_doc_update,
        'button_doc_history': button_doc_history,
        'button_task_create': button_task_create,
        # 'button_task_history': button_task_history,
        #'taskstatus': Dict_DocTaskStatus.objects.filter(is_active=True),
        #'tasktype': Dict_DocTaskType.objects.filter(is_active=True),
        'tskstatus_selectid': tskstatus_selectid,
        'object_list': 'doctask_list',
    })

class DocTaskCreate(AddFilesMixin, CreateView):
    model = DocTask
    form_class = DocTaskForm
    #template_name = 'task_create.html'
    template_name = 'object_form.html'

    def form_valid(self, form):
       form.instance.client_id = self.kwargs['clientid']
       if self.kwargs['parentid'] != 0:
          form.instance.parent_id = self.kwargs['parentid']
       form.instance.author_id = self.request.user.id
       self.object = form.save() # Созадём новую задачу клиента
       af = self.add_files(form, 'crm', 'task') # добавляем файлы из формы (метод из AddFilesMixin)
       historyjson = {"Задача": self.object.name,
                      "Статус": self.object.status.name,
                      "Начало": self.object.datebegin.strftime('%d.%m.%Y %H:%M'),
                      "Окончание": self.object.dateend.strftime('%d.%m.%Y %H:%M'),
                      "Тип в иерархии": self.object.structure_type.name,
                      "Тип": self.object.type.name,
                      "Стоимость": str(self.object.cost),
                      "Выполнен на, %": str(self.object.percentage),
                      "Инициатор": self.object.initiator.name,
                      "Исполнитель": self.object.assigner.username,
                      "Активность": '✓' if self.object.is_active else '-'
                      #, "Участники":self.object.members.username
                     }
       ModelLog.objects.create(componentname='cltsk', modelname="ClientTask", modelobjectid=self.object.id, author=self.object.author, log=json.dumps(historyjson))
       return super().form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(DocTaskCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новая Задача'
       return context

    def get_form_kwargs(self):
       kwargs = super(DocTaskCreate, self).get_form_kwargs()
       kwargs.update({'user': self.request.user, 'action': 'create', 'clientid': self.kwargs['clientid']})
       return kwargs

class DocTaskUpdate(AddFilesMixin, UpdateView):
    model = DocTask
    form_class = DocTaskForm
    #template_name = 'task_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(DocTaskUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Задачу'
       context['files'] = DocVerFile.objects.filter(task_id=self.kwargs['pk'], is_active=True).order_by('uname')
       return context

    def get_form_kwargs(self):
       kwargs = super(DocTaskUpdate, self).get_form_kwargs()
       kwargs.update({'user': self.request.user, 'action': 'update'})
       return kwargs

    def form_valid(self, form):
       self.object = form.save(commit=False)
       af = self.add_files(form, 'crm', 'task') # добавляем файлы из формы (метод из AddFilesMixin)
       old = DocTask.objects.filter(pk=self.object.pk).first() # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
       historyjson = {"Задача":'' if self.object.name == old.name else self.object.name,
                      "Статус":'' if self.object.status.name == old.status.name else self.object.status.name,
                      "Начало":'' if self.object.datebegin == old.datebegin else self.object.datebegin.strftime('%d.%m.%Y %H:%M'),
                      "Окончание":'' if self.object.dateend == old.dateend else self.object.dateend.strftime('%d.%m.%Y %H:%M'),
                      "Тип в иерархии":'' if self.object.structure_type.name == old.structure_type.name else self.object.structure_type.name,
                      "Тип":'' if self.object.type.name == old.type.name else self.object.type.name,
                      "Стоимость":'' if self.object.cost == old.cost else str(self.object.cost),
                      "Выполнен на, %":'' if self.object.percentage == old.percentage else str(self.object.percentage),
                      "Инициатор":'' if self.object.initiator.name == old.initiator.name else self.object.initiator.name,
                      "Исполнитель":'' if self.object.assigner.username == old.assigner.username else self.object.assigner.username,
                      "Активность":'' if self.object.is_active == old.is_active else '✓' if self.object.is_active else '-'
                      #, "Участники":self.members.username
                     }
       ModelLog.objects.create(componentname='cltsk', modelname="ClientTask", modelobjectid=self.object.id, author=self.object.author, log=json.dumps(historyjson))
       return super().form_valid(form)

#def doc_list(request):
#    return render(request, "docdoc_list.html", {'nodes': nodes,})

#def file_list(request):
#    return render(request, "docfile_list.html", {'nodes': nodes,})

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def doctaskfilter(request):
    clientid = request.GET['clientid']
    taskstatus = request.GET['taskstatus']
    tasktype = request.GET['tasktype']
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    #tskstatus_selectid = 0
    if taskstatus == "0":
       # если в выпадающем списке выбрано "Все активные"
       task_list = DocTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid, dateclose__isnull=True)
    else:
       if taskstatus == "-1":
          # если в выпадающем списке выбрано "Все"
          task_list = DocTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid)
       elif taskstatus == "-2":
          # если в выпадающем списке выбрано "Просроченные"
          task_list = DocTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid, dateclose__isnull=True, dateend__lt=datetime.now())
       else:
          task_list = DocTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid, status=taskstatus)
    # *** фильтр по типу ***
    if tasktype != "-1":
       task_list = task_list.filter(Q(type=tasktype))
    # *** фильтр по принадлежности ***
    mytskuser = request.GET['mytaskuser']
    if mytskuser == "0":
       task_list = task_list.filter(Q(client__members__in=[currentuser,]))
    elif mytskuser == "1":
       task_list = task_list.filter(Q(author=request.user.id))
    elif mytskuser == "2":
       task_list = task_list.filter(Q(assigner=request.user.id))
    # *******************************
    nodes = task_list.distinct().order_by()
    object_message = ''
    if len(nodes) == 0:
       object_message = 'Задачи не найдены!'
    return render(request, 'objects_list.html', {'nodes': nodes, 'object_list': 'doctask_list', 'object_message': object_message})

def docver_change(request):
    docverid = request.GET['docverid']
    if docverid == 0:
        return False
    # позиционируемся на нужной версии
    docver = DocVer.objects.filter(id=docverid).first()
    # делаем все версии Документа неактуальными
    DocVer.objects.filter(doc_id=docver.doc_id).update(is_actual=False)
    # делаем текущую версию Документа актуальной
    docver.is_actual = True
    docver.save()
    #return render(request, 'objects_history.html')
    doctasks(request, docver.doc_id)
    return True
    #return render(request, 'doctasks_list.html')