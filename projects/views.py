from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime, date, time
import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import loader, Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist
#from versane.models import Company

from companies.models import Company
from projects.models import Dict_ProjectStatus, Dict_TaskStatus
from projects.models import Project, Task, TaskComment, ProjectStatusLog, TaskStatusLog
from companies.forms import CompanyForm
from .forms import ProjectForm, TaskForm, TaskCommentForm
from .forms import ProjectStatusLog, TaskStatusLog

from .tables import ProjectStatusLogTable, TaskStatusLogTable
from django_tables2 import RequestConfig

from django.contrib.auth.decorators import login_required

from django.db.models import Q, Count, Min, Max, Sum, Avg

#from .utils import ObjectUpdateMixin

#class ProjectsHome(TemplateView):
#   template_name = 'main.html'

class ProjectsList(ListView):
    model = Project
    template_name = 'company_detail.html'

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def projects(request, companyid=0, pk=0):

    if companyid == 0:
       companyid = request.session['_auth_user_currentcompany_id']

    # *** фильтруем по статусу ***
    currentuser = request.user.id
    prjstatus_selectid = 0
    #myprjstatus = 0 # для фильтра "Мои проекты"
    try:
       prjstatus = request.POST['select_projectstatus']
    except:
       project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, dateclose__isnull=True)
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

    current_company = Company.objects.get(id=companyid)

    if pk == 0:
       current_project = 0
       tree_project_id = 0
       root_project_id = 0
       tree_project_id = 0
    else:
       current_project = Project.objects.get(id=pk)
       tree_project_id = current_project.tree_id  
       root_project_id = current_project.get_root().id
       tree_project_id = current_project.tree_id

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
    if current_company in comps:
       button_project_create = 'Добавить'
    return render(request, "company_detail.html", {
                              'nodes': project_list.distinct().order_by(), # для удаления задвоений и восстановления иерархии
                              'current_project': current_project,
                              'root_project_id': root_project_id,
                              'tree_project_id': tree_project_id,
                              'current_company': current_company,
                              'companyid': companyid,
                              'user_companies': comps,
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
                                                })       

class ProjectDetail(DetailView):
    model = Project
    template_name = 'project_detail.html' 

class ProjectCreate(CreateView):    
    model = Project
    form_class = ProjectForm
    #template_name = 'project_create.html'
    template_name = 'object_form.html'

    def form_valid(self, form):
       form.instance.company_id = self.kwargs['companyid']
       if self.kwargs['parentid'] != 0:
          form.instance.parent_id = self.kwargs['parentid']
       form.instance.author_id = self.request.user.id
       return super(ProjectCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(ProjectCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новый Проект'
       return context

    def get_form_kwargs(self):
       kwargs = super(ProjectCreate, self).get_form_kwargs()
       # здесь нужно условие для 'action': 'create'
       kwargs.update({'user': self.request.user, 'action': 'create', 'companyid': self.kwargs['companyid']})
       return kwargs   

class ProjectUpdate(UpdateView):    
    model = Project
    form_class = ProjectForm
    #template_name = 'project_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(ProjectUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Проект'
       return context

    def get_form_kwargs(self):
       kwargs = super(ProjectUpdate, self).get_form_kwargs()
       # здесь нужно условие для 'action': 'update'
       kwargs.update({'user': self.request.user, 'action': 'update'})
       return kwargs

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

    currentproject = Project.objects.get(id=projectid)

    taskcomment_costsum = TaskComment.objects.filter(task__project_id=currentproject.id).aggregate(Sum('cost'))
    taskcomment_timesum = TaskComment.objects.filter(task__project_id=currentproject.id).aggregate(Sum('time'))
    try:
       sec = taskcomment_timesum["time__sum"]*3600
    except:
       sec = 0
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    seconds = sec    
    
    if pk == 0:
       current_task = 0
       tree_task_id = 0  
       root_task_id = 0
       tree_task_id = 0 
    else:
       current_task = Task.objects.get(id=pk)
       tree_task_id = current_task.tree_id  
       root_task_id = current_task.get_root().id
       tree_task_id = current_task.tree_id

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
     
    return render(request, "project_detail.html", {
                              'nodes': task_list.distinct().order_by(), #.order_by('tree_id', 'level', '-dateend'),
                              'current_task': current_task,
                              'root_task_id': root_task_id,
                              'tree_task_id': tree_task_id,
                              'current_project': currentproject,                             
                              'projectid': projectid,
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
                                                })       

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

class TaskCreate(CreateView):    
    model = Task
    form_class = TaskForm
    #template_name = 'task_create.html'
    template_name = 'object_form.html'

    def form_valid(self, form):
       form.instance.project_id = self.kwargs['projectid']
       if self.kwargs['parentid'] != 0:
          form.instance.parent_id = self.kwargs['parentid']
       form.instance.author_id = self.request.user.id
       return super(TaskCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(TaskCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новая Задача'
       return context

    def get_form_kwargs(self):
       kwargs = super(TaskCreate, self).get_form_kwargs()
       kwargs.update({'user': self.request.user, 'action': 'create', 'projectid': self.kwargs['projectid']})
       return kwargs   

class TaskUpdate(UpdateView):    
    model = Task
    form_class = TaskForm
    #template_name = 'task_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(TaskUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Задачу'
       return context

    def get_form_kwargs(self):
       kwargs = super(TaskUpdate, self).get_form_kwargs()
       kwargs.update({'user': self.request.user, 'action': 'update'})
       return kwargs       

#class TaskDelete(DeleteView):    
#    model = Task
#    #form_class = TaskForm
#    template_name = 'task_delete.html'
#    success_url = '/success/' 

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def taskcomments(request, taskid):

    currenttask = Task.objects.get(id=taskid)
    currentuser = request.user.id
    
    taskcomment_costsum = TaskComment.objects.filter(task=taskid).aggregate(Sum('cost'))
    taskcomment_timesum = TaskComment.objects.filter(task=taskid).aggregate(Sum('time'))
    try:
       sec = taskcomment_timesum["time__sum"]*3600
    except:
       sec = 0
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    seconds = sec
    taskcomment_list = TaskComment.objects.filter(Q(author=request.user.id) | Q(task__project__members__in=[currentuser,]), is_active=True, task=taskid)

    button_taskcomment_create = ''
    #button_taskcomment_update = ''
    button_task_create = ''
    button_task_update = ''    
    button_task_history = ''
    is_member = Project.objects.filter(members__in=[currentuser,]).exists()
    if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id or is_member:
       button_task_create = 'Добавить'
       button_task_history = 'История' 
       button_taskcomment_create = 'Добавить'             
       if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id:
          button_task_update = 'Изменить'
     
    return render(request, "task_detail.html", {
                              'nodes': taskcomment_list.distinct().order_by(),
                              #'current_taskcomment': currenttaskcomment,
                              'task': currenttask,
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

class TaskCommentCreate(CreateView):    
    model = TaskComment
    form_class = TaskCommentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(TaskCommentCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новый Комментарий'
       return context

    def form_valid(self, form):
       form.instance.task_id = self.kwargs['taskid']
       form.instance.author_id = self.request.user.id
       return super(TaskCommentCreate, self).form_valid(form)

class TaskCommentUpdate(UpdateView):    
    model = TaskComment
    form_class = TaskCommentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(TaskCommentUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Комментарий'
       return context

#class TaskCommentDelete(DeleteView):    
#    model = TaskComment
#    #form_class = TaskCommentForm
#    #template_name = 'taskcomment_delete.html'
#    success_url = '/success/' 

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def projecthistory(request, pk=0):

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
def taskhistory(request, pk=0):

    if pk == 0:
       current_task = 0
    else:
       current_task = Task.objects.get(id=pk)

    comps = request.session['_auth_user_companies_id']

    nodes = TaskStatusLog.objects.filter(task_id=pk, is_active=True)
    table = TaskStatusLogTable(nodes)    

    return render(request, "task_history.html", {
                              'nodes': nodes, 
                              'current_task': current_task,
                              'user_companies': comps,  
                              'table': table,                                                               
                                                })  

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
            nodes = project_list.order_by().distinct()
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
    nodes = task_list.distinct().order_by()
    object_message = ''
    if len(nodes) == 0:
       object_message = 'Задачи не найдены!'                  
    return render(request, 'objects_list.html', {'nodes': nodes, 'object_list': 'task_list', 'object_message': object_message})           

#def project__filter(request, companyid=0):
#   response = render(
#         request,
#         'projects_list.html',
#         {'nodes': Project.objects.filter(is_active=True, company=companyid).order_by()}
#         )
#  return response   

