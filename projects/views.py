import os
# import socket
from django.conf import settings

from django.urls import reverse_lazy
# from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import datetime, timedelta  #, date, time

import json
import requests
from django.db import connection

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import loader, Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist
# from versane.models import Company

from companies.models import Company
from main.models import ModelLog
from projects.models import Dict_ProjectStatus, Dict_TaskStatus
from projects.models import Project, Task, TaskComment, ProjectFile #, ProjectStatusLog, TaskStatusLog

from companies.forms import CompanyForm
from .forms import ProjectForm, TaskForm, TaskCommentForm
# from .forms import ProjectStatusLog, TaskStatusLog

# from .tables import ProjectStatusLogTable, TaskStatusLogTable
from django_tables2 import RequestConfig

from django.contrib.auth.decorators import login_required

from django.db.models import Q, Count, Min, Max, Sum, Avg

from main.utils import AddFilesMixin #ObjectUpdateMixin

#class ProjectsHome(TemplateView):
#   template_name = 'main.html'

class ProjectsList(ListView):
    model = Project
    template_name = 'company_detail.html'

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def projects(request, companyid=0, pk=0):

    if companyid == 0:
       companyid = request.session['_auth_user_currentcompany_id']

    request.session['_auth_user_currentcomponent'] = 'projects'

    # *** фильтруем по статусу ***
    currentuser = request.user.id
    prjstatus_selectid = 0
    #myprjstatus = 0 # для фильтра "Мои проекты"
    try:
       prjstatus = request.POST['select_projectstatus']
    except:
       project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True,
                                             company=companyid, dateclose__isnull=True)
    else:
       if prjstatus == "0":
          # если в выпадающем списке выбрано "Все активные"
          project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, dateclose__isnull=True)
       else:
          if prjstatus == "-1":
             # если в выпадающем списке выбрано "Все"
             project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid)
          elif prjstatus == "-2":
             # если в выпадающем списке выбрано "Просроченные"
             project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, dateclose__isnull=True, dateend__lt=datetime.now())
          else:             
             project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, status=prjstatus) #, dateclose__isnull=True)
       prjstatus_selectid = prjstatus
    #prjstatus_myselectid = myprjstatus
    # *******************************
    #project_list = project_list.order_by('dateclose')

    len_list = len(project_list)

    current_company = Company.objects.get(id=companyid)
    # *** немного потискал прямые запросы к БД
    #cursor = connection.cursor()
    #sql = 'SELECT * FROM companies_company WHERE id=%s'
    #cursor.execute(sql, [companyid])
    #current_company = cursor.fetchone() #.fetchall()
    #idcomp = '''id=companyid'''
    #current_company = Company.objects.get(idcomp)
    #print(current_company)
    #print(current_company[9])
    # ***

    obj_files_rights = 0

    if pk == 0:
       current_project = 0
       tree_project_id = 0
       root_project_id = 0
       #tree_project_id = 0
    else:
       current_project = Project.objects.filter(id=pk).first().select_related("company", "author", "assigner", "status", "type", "structure_type",
                                                                   "currency") #.prefetch_related("members")
       #idpk = 'id=pk'
       #current_project = Project.objects.get({idpk})
       tree_project_id = current_project.tree_id  
       root_project_id = current_project.get_root().id
       #tree_project_id = current_project.tree_id
       if currentuser == current_project.author_id or currentuser == current_project.assigner_id:
           obj_files_rights = 1

    button_company_select = ''
    button_company_create = ''
    button_company_update = ''
    button_project_create = ''

    # здесь нужно условие для button_company_create
    # если текущий пользователь не является автором созданной текущей организации, то добавлять и изменять Компанию можно только в приложении Организации
    #button_company_create = 'Добавить'
    # здесь нужно условие для button_company_update
    #button_company_update = 'Изменить'
    # здесь нужно условие для button_project_create
    #button_project_create = 'Добавить'
    # здесь нужно условие для button_company_select
    comps = request.session['_auth_user_companies_id']
    if len(comps) > 1:
       button_company_select = 'Сменить организацию'        
    if currentuser == current_company.author_id:
       button_company_create = 'Добавить'
       button_company_update = 'Изменить'
       button_project_create = 'Добавить'        
    if current_company.id in comps:
       button_project_create = 'Добавить'

    project_list = project_list.select_related("company", "author", "assigner", "status", "type", "structure_type", "currency") #.prefetch_related(
        #"members")

    return render(request, "company_detail.html", {
                              'nodes': project_list.distinct(), #.order_by(), # для удаления задвоений и восстановления иерархии
                              'current_project': current_project,
                              'root_project_id': root_project_id,
                              'tree_project_id': tree_project_id,
                              'current_company': current_company,
                              'companyid': companyid,
                              'user_companies': comps,
                              'component_name': 'projects',
                              'obj_files_rights': obj_files_rights,
                              'button_company_select': button_company_select,
                              'button_company_create': button_company_create,
                              'button_company_update': button_company_update,
                              'button_project_create': button_project_create,
                              #'button_project_history': button_project_history,
                              'projectstatus': Dict_ProjectStatus.objects.filter(is_active=True),
                              'prjstatus_selectid': prjstatus_selectid,
                              #'prjstatus_myselectid': prjstatus_myselectid,                              
                              'object_list': 'project_list',
                              #'select_projectstatus': select_projectstatus,
                              'len_list': len_list,
                              #'fullpath': os.path.join(settings.MEDIA_ROOT, '///'),
                                                })       

class ProjectDetail(DetailView):
    model = Project
    template_name = 'project_detail.html' 

class ProjectCreate(AddFilesMixin, CreateView):    
    model = Project
    form_class = ProjectForm
    #template_name = 'project_create.html'
    template_name = 'object_form.html'

    def form_valid(self, form):
        form.instance.company_id = self.kwargs['companyid']
        if self.kwargs['parentid'] != 0:
           form.instance.parent_id = self.kwargs['parentid']
        form.instance.author_id = self.request.user.id
        self.object = form.save() # Созадём новый проект
        af = self.add_files(form, 'project', 'project') # добавляем файлы из формы (метод из AddFilesMixin)
        # формируем строку из Участников
        memb = self.object.members.values_list('id', 'username').all()
        membersstr = ''
        for mem in memb:
            membersstr = membersstr + mem[1] + ','
        # Делаем первую запись в историю изменений проекта
        historyjson = {"Проект": self.object.name,
                       "Статус": self.object.status.name, 
                       "Начало": self.object.datebegin.strftime('%d.%m.%Y'), 
                       "Окончание": self.object.dateend.strftime('%d.%m.%Y'),
                       "Тип в иерархии": self.object.structure_type.name,
                       "Тип": self.object.type.name,
                       "Стоимость": str(self.object.cost),
                       "Валюта": str(self.object.currency.code_char),
                       "Выполнен на, %": str(self.object.percentage),
                       "Исполнитель": self.object.assigner.username,
                       "Участники": membersstr,
                       "Активность": '✓' if self.object.is_active else '-'
                      }
        ModelLog.objects.create(componentname='prj', modelname="Project", modelobjectid=self.object.id, author=self.object.author, log=json.dumps(historyjson))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Новый Проект'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # здесь нужно условие для 'action': 'create'
        kwargs.update({'user': self.request.user, 'action': 'create', 'companyid': self.kwargs['companyid']})
        return kwargs   

class ProjectUpdate(AddFilesMixin, UpdateView):    
      model = Project
      form_class = ProjectForm
      #template_name = 'project_update.html'
      template_name = 'object_form.html'
  
      def get_context_data(self, **kwargs):
          #context = super(ProjectUpdate, self).get_context_data(**kwargs)
          context = super().get_context_data(**kwargs)
          context['header'] = 'Изменить Проект'
          #kwargs = super(ProjectUpdate, self).get_form_kwargs()
          kwargs = super().get_form_kwargs()
          context['files'] = ProjectFile.objects.filter(project_id=self.kwargs['pk'], is_active=True).order_by('uname')
          #print(context)
          #print(kwargs)
          return context
  
      def get_form_kwargs(self):
          #kwargs = super(ProjectUpdate, self).get_form_kwargs()
          kwargs = super().get_form_kwargs()
          # здесь нужно условие для 'action': 'update'
          kwargs.update({'user': self.request.user, 'action': 'update'})
          return kwargs       
  
      def form_valid(self, form):        
          self.object = form.save(commit=False) # без commit=False происходит вызов save() Модели
          af = self.add_files(form, 'project', 'project') # добавляем файлы из формы (метод из AddFilesMixin)
          # Получаем старые значения для дальнейшей проверки на изменения
          old = Project.objects.filter(pk=self.object.pk).first() # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
          old_memb = old.members.values_list('id', 'username').all()
          old_memb_count = old_memb.count()
          old_memb_list = list(old_memb)
          self.object = form.save()
          # записываем новых Участников
          memb = self.object.members.values_list('id', 'username').all()
          memb_count = memb.count()
          is_members_changed = False
          if old_memb_count != memb_count:
              is_members_changed = True
          #print(list(memb))
          membersstr = ''
          for mem in memb:
              membersstr = membersstr + mem[1] + ','
              if is_members_changed == False:
                  if old_memb_list.count(mem) == 0:
                      is_members_changed = True
          historyjson = {"Проект":'' if self.object.name == old.name else self.object.name,
                         "Статус":'' if self.object.status.name == old.status.name else self.object.status.name, 
                         "Начало":'' if self.object.datebegin == old.datebegin else self.object.datebegin.strftime('%d.%m.%Y'), 
                         "Окончание":'' if self.object.dateend == old.dateend else self.object.dateend.strftime('%d.%m.%Y'),
                         "Тип в иерархии":'' if self.object.structure_type.name == old.structure_type.name else self.object.structure_type.name,
                         "Тип":'' if self.object.type.name == old.type.name else self.object.type.name,
                         "Стоимость":'' if self.object.cost == old.cost else str(self.object.cost),
                         "Валюта":'' if self.object.currency.code_char == old.currency.code_char else str(self.object.currency.code_char),
                         "Выполнен на, %":'' if self.object.percentage == old.percentage else str(self.object.percentage),
                         "Исполнитель":'' if self.object.assigner.username == old.assigner.username else self.object.assigner.username,
                         #"Участники": self.object.members.username,
                         "Участники": '' if is_members_changed == False else membersstr,
                         "Активность":'' if self.object.is_active == old.is_active else '✓' if self.object.is_active else '-'
                        }
         #  print(historyjson)
          ModelLog.objects.create(componentname='prj', modelname="Project", modelobjectid=self.object.id, author=self.object.author, log=json.dumps(historyjson))          
          return super().form_valid(form) #super(ProjectUpdate, self).form_valid(form)

#class ProjectDelete(DeleteView):    
#    model = Project
#    #form_class = ProjectForm
#    template_name = 'project_delete.html'
#    success_url = '/success/' 

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def tasks(request, projectid=0, pk=0):

    # *** фильтруем по статусу ***
    currentuser = request.user.id
    tskstatus_selectid = 0

    try:
       tskstatus = request.POST['select_taskstatus']
    except:
       task_list = Task.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(project__members__in=[currentuser,]), is_active=True, project=projectid, dateclose__isnull=True)
    else:
       if tskstatus == "0":
          # если в выпадающем списке выбрано "Все активные"
          task_list = Task.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(project__members__in=[currentuser,]), is_active=True, project=projectid, dateclose__isnull=True)
       else:
          if tskstatus == "-1":
             # если в выпадающем списке выбрано "Все"
             task_list = Task.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(project__members__in=[currentuser,]), is_active=True, project=projectid)
          elif tskstatus == "-2":
             # если в выпадающем списке выбрано "Просроченные"
             task_list = Task.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(project__members__in=[currentuser,]), is_active=True, project=projectid, dateclose__isnull=True, dateend__lt=datetime.now())
          else:             
             task_list = Task.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(project__members__in=[currentuser,]), is_active=True, project=projectid, status=tskstatus) #, dateclose__isnull=True)

       tskstatus_selectid = tskstatus
    # *******************************

    len_list = len(task_list)
    #print(len_list)    

    currentproject = Project.objects.filter(id=projectid).select_related("company", "author", "assigner", "status", "type", "structure_type",
                                                                         "currency").first()
    #currentproject = Project.objects.filter(id=projectid).first()

    #taskcomment_costsum = TaskComment.objects.filter(task__project_id=currentproject.id).aggregate(Sum('cost'))
    #taskcomment_timesum = TaskComment.objects.filter(task__project_id=currentproject.id).aggregate(Sum('time'))
    taskcomment_costsum = currentproject.costsum
    taskcomment_timesum = currentproject.timesum
    try:
       sec = taskcomment_timesum["time__sum"]*3600
    except:
       sec = 0
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    seconds = sec

    obj_files_rights = 0

    if pk == 0:
       current_task = 0
       root_task_id = 0
       tree_task_id = 0
       if currentuser == currentproject.author_id or currentuser == currentproject.assigner_id:
           obj_files_rights = 1
    else:
       current_task = Task.objects.filter(id=pk).select_related("project", "author", "assigner", "status", "type", "structure_type").first()
       #current_task = Task.objects.filter(id=pk).first()
       root_task_id = current_task.get_root().id
       tree_task_id = current_task.tree_id
       if currentuser == current_task.author_id or currentuser == current_task.assigner_id:
           obj_files_rights = 1

    button_project_create = ''
    button_project_update = ''
    button_project_history = ''     
    button_task_create = ''

    is_member = Project.objects.filter(members__in=[currentuser,]).exists()
    if currentuser == currentproject.author_id or currentuser == currentproject.assigner_id or is_member:
       button_project_create = 'Добавить'
       button_project_history = 'История' 
       button_task_create = 'Добавить'             
       if currentuser == currentproject.author_id or currentuser == currentproject.assigner_id:
          button_project_update = 'Изменить'

    task_list = task_list.select_related("project", "author", "assigner", "status", "type", "structure_type")
     
    return render(request, "project_detail.html", {
                              'nodes': task_list.distinct(), #.order_by(), #.order_by('tree_id', 'level', '-dateend'),
                              'current_task': current_task,
                              'root_task_id': root_task_id,
                              'tree_task_id': tree_task_id,
                              'current_project': currentproject,                             
                              'projectid': projectid,
                              'obj_files_rights': obj_files_rights,
                              'files': ProjectFile.objects.filter(project=currentproject, is_active=True).order_by('uname'),
                              'component_name': 'projects',
                              'objtype': 'prj',
                              'media_path': settings.MEDIA_URL,                              
                              'user_companies': request.session['_auth_user_companies_id'],                              
                              'button_project_create': button_project_create,
                              'button_project_update': button_project_update,
                              'button_project_history': button_project_history,
                              'button_task_create': button_task_create,
                              #'button_task_history': button_task_history,                              
                              'taskstatus': Dict_TaskStatus.objects.filter(is_active=True),
                              'tskstatus_selectid': tskstatus_selectid,
                              'object_list': 'task_list',
                              'taskcomment_costsum': taskcomment_costsum,
                              'taskcomment_timesum': taskcomment_timesum,  
                              'hours': hours, 'minutes': minutes, 'seconds': seconds,
                              'len_list': len_list,
                                                })       
"""
class TaskDetail___(DetailView):
   model = Task
   template_name = 'task_detail.html'  
    
   def get_context_data(self, **kwargs):
       context = super(TaskDetail, self).get_context_data(**kwargs)
       currentuser = request.user.id
       button_task_create = ''
       button_task_update = ''
       button_task_history = '' 
       button_taskcomment_create = ''
       #return super(TaskDetail, self).get_context_data(**kwargs)
       is_member = Project.objects.filter(members__in=[currentuser,]).exists()
       if currentuser == self.author_id or currentuser == self.assigner_id or is_member:
          button_task_create = 'Добавить'
          button_task_history = 'История' 
          button_taskcomment_create = 'Добавить'             
          if currentuser == self.author_id:
             button_task_update = 'Изменить' 
       context['button_task_create'] = button_task_create
       context['button_task_update'] = button_task_update
       context['button_task_history'] = button_task_history
       context['button_taskcomment_create'] = button_taskcomment_create      
       return context
"""
class TaskCreate(AddFilesMixin, CreateView):    
    model = Task
    form_class = TaskForm
    #template_name = 'task_create.html'
    template_name = 'object_form.html'

    #def form_valid(self, form):
    #   form.instance.project_id = self.kwargs['projectid']
    #   if self.kwargs['parentid'] != 0:
    #      form.instance.parent_id = self.kwargs['parentid']
    #   form.instance.author_id = self.request.user.id
    #   return super().form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(TaskCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новая Задача'
       return context      

    def get_form_kwargs(self):
       kwargs = super().get_form_kwargs()
       kwargs.update({'user': self.request.user, 'action': 'create', 'projectid': self.kwargs['projectid']})
       return kwargs

    def form_valid(self, form):
       form.instance.project_id = self.kwargs['projectid']
       if self.kwargs['parentid'] != 0:
          form.instance.parent_id = self.kwargs['parentid']
       form.instance.author_id = self.request.user.id
       #self.object = form.save(commit=False) # без commit=False происходит вызов save() Модели       
       self.object = form.save()
       af = self.add_files(form, 'project', 'task') # добавляем файлы из формы (метод из AddFilesMixin)
       historyjson = {"Задача": self.object.name,
                      "Статус": self.object.status.name, 
                      "Начало": self.object.datebegin.strftime('%d.%m.%Y %H:%M'), 
                      "Окончание": self.object.dateend.strftime('%d.%m.%Y %H:%M'),
                      "Тип в иерархии": self.object.structure_type.name,
                      "Тип": self.object.type.name,
                      "Стоимость": str(self.object.cost),
                      "Выполнен на, %": str(self.object.percentage),
                      "Исполнитель": self.object.assigner.username,
                      "Активность": '✓' if self.object.is_active else '-'
                      #, "Участники":self.object.members.username
                     }
       ModelLog.objects.create(componentname='tsk', modelname="Task", modelobjectid=self.object.id, author=self.object.author, log=json.dumps(historyjson))       
       return super().form_valid(form)        

class TaskUpdate(AddFilesMixin, UpdateView):    
    model = Task
    form_class = TaskForm
    #template_name = 'task_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['header'] = 'Изменить Задачу'
       kwargs = super().get_form_kwargs()      
       context['files'] = ProjectFile.objects.filter(task_id=self.kwargs['pk'], is_active=True).order_by('uname')       
       return context

    def get_form_kwargs(self):
       kwargs = super().get_form_kwargs()
       kwargs.update({'user': self.request.user, 'action': 'update'})
       return kwargs       

    def form_valid(self, form):
       self.object = form.save(commit=False) # без commit=False происходит вызов save() Модели
       af = self.add_files(form, 'project', 'task') # добавляем файлы из формы (метод из AddFilesMixin)
       old = Task.objects.filter(pk=self.object.pk).first()
       historyjson = {"Задача":'' if self.object.name == old.name else self.object.name,
                      "Статус":'' if self.object.status.name == old.status.name else self.object.status.name, 
                      "Начало":'' if self.object.datebegin == old.datebegin else self.object.datebegin.strftime('%d.%m.%Y %H:%M'), 
                      "Окончание":'' if self.object.dateend == old.dateend else self.object.dateend.strftime('%d.%m.%Y %H:%M'),                
                      "Тип в иерархии":'' if self.object.structure_type.name == old.structure_type.name else self.object.structure_type.name,
                      "Тип":'' if self.object.type.name == old.type.name else self.object.type.name,
                      "Стоимость":'' if self.object.cost == old.cost else str(self.object.cost),
                      "Выполнен на, %":'' if self.object.percentage == old.percentage else str(self.object.percentage),
                      "Исполнитель":'' if self.object.assigner.username == old.assigner.username else self.object.assigner.username,
                      #"Участники": '' if is_members_changed == False else membersstr,
                      "Активность":'' if self.object.is_active == old.is_active else '✓' if self.object.is_active else '-'
                     }
       ModelLog.objects.create(componentname='tsk', modelname="Task", modelobjectid=self.object.id, author=self.object.author, log=json.dumps(historyjson))                            
       return super().form_valid(form) #super(TaskUpdate, self).form_valid(form)

#class TaskDelete(DeleteView):    
#    model = Task
#    #form_class = TaskForm
#    template_name = 'task_delete.html'
#    success_url = '/success/' 

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def taskcomments(request, taskid):

    currenttask = Task.objects.filter(id=taskid).select_related("project", "author", "assigner", "status", "type", "structure_type").first()
    currentuser = request.user.id
    
    #taskcomment_costsum = TaskComment.objects.filter(task=taskid).aggregate(Sum('cost'))
    #taskcomment_timesum = TaskComment.objects.filter(task=taskid).aggregate(Sum('time'))
    taskcomment_costsum = currenttask.costsum
    taskcomment_timesum = currenttask.timesum
    try:
       sec = taskcomment_timesum["time__sum"]*3600
    except:
       sec = 0
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    seconds = sec
    taskcomment_list = TaskComment.objects.filter(Q(author=request.user.id) | Q(task__project__members__in=[currentuser,]), is_active=True, task=taskid).select_related("task", "author")

    button_taskcomment_create = ''
    #button_taskcomment_update = ''
    button_task_create = ''
    button_task_update = ''    
    button_task_history = ''
    is_member = Project.objects.filter(members__in=[currentuser,]).exists()
    obj_files_rights = 0
    if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id:
        obj_files_rights = 1
    if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id or is_member:
        button_task_create = 'Добавить'
        button_task_history = 'История'
        button_taskcomment_create = 'Добавить'
        if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id:
            button_task_update = 'Изменить'

    return render(request, "task_detail.html", {
                              'nodes': taskcomment_list.distinct().order_by(),
                              #'node_files': n_files,
                              #'current_taskcomment': currenttaskcomment,
                              'task': currenttask,
                              'obj_files_rights': obj_files_rights,
                              'files': ProjectFile.objects.filter(task=currenttask, is_active=True).order_by('uname'),
                              'objtype': 'prjtsk',
                              'media_path': settings.MEDIA_URL,
                              'button_task_create': button_task_create,
                              'button_task_update': button_task_update,
                              'button_task_history': button_task_history,
                              'taskcomment_costsum': taskcomment_costsum,
                              'taskcomment_timesum': taskcomment_timesum,
                              'hours': hours, 'minutes': minutes, 'seconds': seconds,                            
                              'button_taskcomment_create': button_taskcomment_create,
                                                })      

class TaskCommentDetail(DetailView):
    model = TaskComment
    template_name = 'taskcomment_detail.html'

class TaskCommentCreate(AddFilesMixin, CreateView):    
    model = TaskComment
    form_class = TaskCommentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['header'] = 'Новый Комментарий'
       return context

    def form_valid(self, form):
       form.instance.task_id = self.kwargs['taskid']
       form.instance.author_id = self.request.user.id
       self.object = form.save()
       af = self.add_files(form, 'project', 'taskcomment') # добавляем файлы из формы (метод из AddFilesMixin)
       return super().form_valid(form)       

class TaskCommentUpdate(UpdateView):    
    model = TaskComment
    form_class = TaskCommentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['header'] = 'Изменить Комментарий'
       kwargs = super().get_form_kwargs()
       context['files'] = ProjectFile.objects.filter(taskcomment_id=self.kwargs['pk'], is_active=True).order_by('uname')       
       return context

#class TaskCommentDelete(DeleteView):    
#    model = TaskComment
#    #form_class = TaskCommentForm
#    #template_name = 'taskcomment_delete.html'
#    success_url = '/success/' 

"""
@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def projecthistory_(request, pk=0):

    #if companyid == 0:
    #   companyid = request.session['_auth_user_currentcompany_id']
    #current_company = Company.objects.get(id=companyid)

    if pk == 0:
       current_project = 0
    else:
       current_project = Project.objects.get(id=pk)

    comps = request.session['_auth_user_companies_id']

    nodes = ProjectStatusLog.objects.filter(project_id=pk, is_active=True)
    table = ProjectStatusLogTable(nodes)

    RequestConfig(request).configure(table)    

    return render(request, "project_history.html", {
                              'nodes': nodes, 
                              'current_project':current_project,
                              #'root_project_id':root_project_id,
                              #'tree_project_id':tree_project_id,
                              #'current_company':current_company,
                              #'companyid':companyid,
                              'user_companies': comps,
                              'table': table,                                                           
                                                })

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def projecthistory__(request, pk=0):

    if pk == 0:
       current_project = 0
    else:
       current_project = Project.objects.get(id=pk)

    comps = request.session['_auth_user_companies_id']

    # формируем массив заголовков
    #row = ModelLog.objects.filter(modelobjectid=pk, is_active=True).first()
    #row = ModelLog.objects.get(modelobjectid=pk, is_active=True)
    #titles = json.loads(row.log).items()

    nodes = ModelLog.objects.filter(modelobjectid=pk, is_active=True) #.order_by()
    
    i = -1
    mas = []
    for node in nodes:
       i += 1
       mas.append(json.loads(node.log).items())
       #print(mas[i])           
       
    return render(request, "project_history.html", {
                              #'titles': titles,
                              'nodes': nodes,
                              'mas': mas,
                              'current_project':current_project,
                              'user_companies': comps,
                              #'table': table,                                                           
                                                })  

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def taskhistory(request, pk=0):

    if pk == 0:
       current_task = 0
    else:
       current_task = Task.objects.get(id=pk)

    comps = request.session['_auth_user_companies_id']

    nodes = TaskStatusLog.objects.filter(task_id=pk, is_active=True)
    table = TaskStatusLogTable(nodes)

    RequestConfig(request).configure(table)        

    return render(request, "task_history.html", {
                              'nodes': nodes, 
                              'current_task': current_task,
                              'user_companies': comps,  
                              'table': table,                                                               
                                                })  
"""

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def projectfilter(request):
    #if request.user.is_authenticated():
            companyid = request.GET['companyid']
            prjstatus = request.GET['projectstatus']
            if companyid == 0:
               companyid = request.session['_auth_user_currentcompany_id']
            # *** фильтруем по статусу ***
            currentuser = request.user.id
            if prjstatus == "0":
               # если в выпадающем списке выбрано "Все активные"
               project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, dateclose__isnull=True) #.filter(id__in=[project.id for project in Project.objects.all() if project.is_leaf_node()])
            else:
               if prjstatus == "-1":
                  # если в выпадающем списке выбрано "Все"
                  project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid) #.filter(id__in=[project.id for project in Project.objects.all() if project.is_leaf_node()])
               elif prjstatus == "-2":
                  # если в выпадающем списке выбрано "Просроченные"
                  project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, dateclose__isnull=True, dateend__lt=datetime.now())                         
               else:   
                  project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, status=prjstatus) #, dateclose__isnull=True)
            # *******************************
            #project_list = Project.objects.filter(is_active=True, company=companyid, status=prjstatus, dateclose__isnull=True) 
            #project_list = Project.objects.filter(id__in=[project.id for project in Project.objects.all() if project.is_leaf_node()])
            # фильтр по принадлежности
            myprjuser = request.GET['myprojectuser']
            if myprjuser == "0":
               project_list = project_list.filter(Q(members__in=[currentuser,]))
            elif myprjuser == "1":
               project_list = project_list.filter(Q(author=request.user.id))               
            elif myprjuser == "2":
               project_list = project_list.filter(Q(assigner=request.user.id)) 
            #nodes = project_list.order_by().distinct()
            nodes = project_list.select_related("company", "author", "assigner", "status", "type", "structure_type", "currency").distinct()
            object_message = ''
            if len(nodes) == 0:
               object_message = 'Проекты не найдены!'
            #print(project_list)        
            #print(prjstatus)
            #print(len(nodes))       
            #return HttpResponse(json.dumps(nodes), content_type='application/json')
            #return JsonResponse({'message': 'Это message!'})
            return render(request, 'objects_list.html', {'nodes': nodes, 'object_list': 'project_list', 'object_message': object_message})           
    #else:
    #    return JsonResponse({'error': 'Only authenticated users'}, status=404) 
        #return render(request, 'projects_list.html', 'Информация недоступна') 

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def taskfilter(request):
    projectid = request.GET['projectid']
    taskstatus = request.GET['taskstatus']
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    #tskstatus_selectid = 0
    if taskstatus == "0":
       # если в выпадающем списке выбрано "Все активные"
       task_list = Task.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(project__members__in=[currentuser,]), is_active=True, project=projectid, dateclose__isnull=True)
    else:
       if taskstatus == "-1":
          # если в выпадающем списке выбрано "Все"
          task_list = Task.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(project__members__in=[currentuser,]), is_active=True, project=projectid)
       elif taskstatus == "-2":
          # если в выпадающем списке выбрано "Просроченные"
          task_list = Task.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(project__members__in=[currentuser,]), is_active=True, project=projectid, dateclose__isnull=True, dateend__lt=datetime.now())                         
       else:             
          task_list = Task.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(project__members__in=[currentuser,]), is_active=True, project=projectid, status=taskstatus)
    # фильтр по принадлежности    
    mytskuser = request.GET['mytaskuser']
    if mytskuser == "0":
       task_list = task_list.filter(Q(project__members__in=[currentuser,]))
    elif mytskuser == "1":
       task_list = task_list.filter(Q(author=request.user.id))               
    elif mytskuser == "2":
       task_list = task_list.filter(Q(assigner=request.user.id)) 
    # *******************************           
    nodes = task_list.select_related("project", "author", "assigner", "status", "type", "structure_type").distinct() #.order_by()
    object_message = ''
    if len(nodes) == 0:
       object_message = 'Задачи не найдены!'                  
    return render(request, 'objects_list.html', {'nodes': nodes, 'object_list': 'task_list', 'object_message': object_message})           


# for Dashboard
def projects_tasks(request):

   # companyid = request.session['_auth_user_currentcompany_id']
   currentuser = request.user.id
   companies_id = request.session["_auth_user_companies_id"]
   date_end = datetime.now() + timedelta(days=10)

   """
   Списки Проектов и Задач конкретного пользователя выводятся для всех Организаций из его списка доступных
   """      

   projects_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser, ]),
                                          company__in=companies_id, is_active=True,
                                          dateclose__isnull=True, dateend__lte=date_end).select_related('type', 'status', 'assigner',
                                                                                                      'author').order_by('dateend', 'type').distinct()
   
   projects_tasks_list = Task.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(project__members__in=[currentuser, ]),
                                             project__company__in=companies_id,
                                             is_active=True, dateclose__isnull=True, dateend__lte=date_end).select_related('project', 'type', 'status',
                                                                                                                           'assigner',
                                                                                                                           'author').order_by('dateend').distinct()

   # print(projects_list, projects_tasks_list)

   return (projects_list, projects_tasks_list)
