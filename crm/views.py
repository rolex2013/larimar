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
#from clients.models import Dict_clientStatus, Dict_TaskStatus
from companies.forms import CompanyForm

from crm.models import Client, Dict_ClientStatus, Dict_ClientType
from crm.models import ClientTask, ClientTaskComment, Dict_ClientTaskStatus, Dict_ClientTaskType #, ClientStatusLog, TaskStatusLog
#from .forms import clientForm, TaskForm, TaskCommentForm
#from .forms import clientStatusLog, TaskStatusLog
from .forms import ClientForm, ClientTaskForm, ClientTaskCommentForm

from .tables import ClientTable, ClientStatusLogTable, ClientTaskStatusLogTable
from django_tables2 import RequestConfig

from django.contrib.auth.decorators import login_required

from django.db.models import Q, Count, Min, Max, Sum, Avg


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clients(request, companyid=0, pk=0):

    if companyid == 0:
       companyid = request.session['_auth_user_currentcompany_id']

    request.session['_auth_user_currentcomponent'] = 'crm'

    # *** фильтруем по статусу ***
    currentuser = request.user.id
    clntstatus_selectid = 0
    #myclntstatus = 0 # для фильтра "Мои клиенты"
    try:
       clntstatus = request.POST['select_clientstatus']
    except:
       client_list = Client.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, dateclose__isnull=True)
    else:
       if clntstatus == "0":
          # если в выпадающем списке выбрано "Все активные"
          client_list = Client.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, dateclose__isnull=True)
       else:
          if clntstatus == "-1":
             # если в выпадающем списке выбрано "Все"
             client_list = Client.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid)
          elif clntstatus == "-2":
             # если в выпадающем списке выбрано "Просроченные"
             client_list = Client.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, dateclose__isnull=True, dateend__lt=datetime.now())                         
          else:             
             client_list = Client.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, status=clntstatus) #, dateclose__isnull=True)
       clntstatus_selectid = clntstatus
    #clntstatus_myselectid = myclntstatus
    # *******************************
    #client_list = client_list.order_by('dateclose')

    current_company = Company.objects.get(id=companyid)

    if pk == 0:
       current_client = 0
       #tree_client_id = 0
       #root_client_id = 0
    else:
       current_client = Client.objects.get(id=pk)
       #tree_client_id = current_client.tree_id  
       #root_client_id = current_client.get_root().id

    button_company_select = ''
    button_company_create = ''
    button_company_update = ''
    button_client_create = ''

    # здесь нужно условие для button_company_create
    # если текущий пользователь не является автором созданной текущей организации, то добавлять и изменять Компанию можно только в приложении Организации
    #button_company_create = 'Добавить'
    # здесь нужно условие для button_company_update
    #button_company_update = 'Изменить'
    # здесь нужно условие для button_client_create
    #button_client_create = 'Добавить'
    # здесь нужно условие для button_company_select
    comps = request.session['_auth_user_companies_id']
    if len(comps) > 1:
       button_company_select = 'Сменить организацию'        
    if currentuser == current_company.author_id:
       button_company_create = 'Добавить'
       button_company_update = 'Изменить'
       button_client_create = 'Добавить'        
    if current_company in comps:
       button_client_create = 'Добавить'
    nodes = client_list.distinct().order_by()
    #table = ClientTable(nodes, c1_name='Клиент')
    #table = ClientTable(nodes)
    return render(request, "company_detail.html", {
                              'nodes': nodes,
                              'current_client': current_client,
                              'current_company': current_company,
                              'companyid': companyid,
                              'user_companies': comps,
                              'button_company_select': button_company_select,
                              'button_company_create': button_company_create,
                              'button_company_update': button_company_update,
                              'button_client_create': button_client_create,
                              #'button_client_history': button_client_history,
                              'clientstatus': Dict_ClientStatus.objects.filter(is_active=True),
                              'clienttype': Dict_ClientType.objects.filter(is_active=True),
                              'clntstatus_selectid': clntstatus_selectid,
                              #'clntstatus_myselectid': clntstatus_myselectid,                              
                              'object_list': 'client_list',
                              #'select_clientstatus': select_clientstatus,
                              'component_name': 'crm',
                              #'table': table,
                                                })  

class ClientCreate(CreateView):    
    model = Client
    form_class = ClientForm
    #template_name = 'client_create.html'
    template_name = 'object_form.html'

    def form_valid(self, form):
       form.instance.company_id = self.kwargs['companyid']
       #if self.kwargs['parentid'] != 0:
       #   form.instance.parent_id = self.kwargs['parentid']
       form.instance.author_id = self.request.user.id
       return super(ClientCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(ClientCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новый Клиент'
       return context

    def get_form_kwargs(self):
       kwargs = super(ClientCreate, self).get_form_kwargs()
       # здесь нужно условие для 'action': 'create'
       kwargs.update({'user': self.request.user, 'action': 'create', 'companyid': self.kwargs['companyid']})
       return kwargs

class ClientUpdate(UpdateView):    
    model = Client
    form_class = ClientForm
    #template_name = 'client_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(ClientUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Клиента'
       return context

    def get_form_kwargs(self):
       kwargs = super(ClientUpdate, self).get_form_kwargs()
       # здесь нужно условие для 'action': 'update'
       kwargs.update({'user': self.request.user, 'action': 'update'})
       return kwargs



@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienttasks(request, clientid=0, pk=0):

    # *** фильтруем по статусу ***
    currentuser = request.user.id
    tskstatus_selectid = 0
    try:
       tskstatus = request.POST['select_taskstatus']
    except:
       task_list = ClientTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid, dateclose__isnull=True)
    else:
       if tskstatus == "0":
          # если в выпадающем списке выбрано "Все активные"
          task_list = ClientTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid, dateclose__isnull=True)
       else:
          if tskstatus == "-1":
             # если в выпадающем списке выбрано "Все"
             task_list = ClientTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid)
          elif tskstatus == "-2":
             # если в выпадающем списке выбрано "Просроченные"
             task_list = ClientTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid, dateclose__isnull=True, dateend__lt=datetime.now())                         
          else:             
             task_list = ClientTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid, status=tskstatus) #, dateclose__isnull=True)
       tskstatus_selectid = tskstatus
    # *******************************

    currentclient = Client.objects.get(id=clientid)

    taskcomment_costsum = ClientTaskComment.objects.filter(task__client_id=currentclient.id).aggregate(Sum('cost'))
    taskcomment_timesum = ClientTaskComment.objects.filter(task__client_id=currentclient.id).aggregate(Sum('time'))
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
       current_task = ClientTask.objects.get(id=pk)
       tree_task_id = current_task.tree_id  
       root_task_id = current_task.get_root().id
       tree_task_id = current_task.tree_id

    button_client_create = ''
    button_client_update = ''
    button_client_history = ''     
    button_task_create = ''

    is_member = Client.objects.filter(members__in=[currentuser,]).exists()
    if currentuser == currentclient.author_id or currentuser == currentclient.assigner_id or is_member:
       button_client_create = 'Добавить'
       button_client_history = 'История' 
       button_task_create = 'Добавить'             
       if currentuser == currentclient.author_id or currentuser == currentclient.assigner_id:
          button_client_update = 'Изменить'    
     
    return render(request, "client_detail.html", {
                              'nodes': task_list.distinct().order_by(), #.order_by('tree_id', 'level', '-dateend'),
                              'current_task': current_task,
                              'root_task_id': root_task_id,
                              'tree_task_id': tree_task_id,
                              'current_client': currentclient,                             
                              'clientid': clientid,
                              'user_companies': request.session['_auth_user_companies_id'],                              
                              'button_client_create': button_client_create,
                              'button_client_update': button_client_update,
                              'button_client_history': button_client_history,
                              'button_task_create': button_task_create,
                              #'button_task_history': button_task_history,                              
                              'taskstatus': Dict_ClientTaskStatus.objects.filter(is_active=True),
                              'tskstatus_selectid': tskstatus_selectid,
                              'object_list': 'clienttask_list',
                              'taskcomment_costsum': taskcomment_costsum,
                              'taskcomment_timesum': taskcomment_timesum,  
                              'hours': hours, 'minutes': minutes, 'seconds': seconds,                                   
                                                })

class ClientTaskCreate(CreateView):    
    model = ClientTask
    form_class = ClientTaskForm
    #template_name = 'task_create.html'
    template_name = 'object_form.html'

    def form_valid(self, form):
       form.instance.client_id = self.kwargs['clientid']
       if self.kwargs['parentid'] != 0:
          form.instance.parent_id = self.kwargs['parentid']
       form.instance.author_id = self.request.user.id
       return super(ClientTaskCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(ClientTaskCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новая Задача'
       return context

    def get_form_kwargs(self):
       kwargs = super(ClientTaskCreate, self).get_form_kwargs()
       kwargs.update({'user': self.request.user, 'action': 'create', 'clientid': self.kwargs['clientid']})
       return kwargs   

class ClientTaskUpdate(UpdateView):    
    model = ClientTask
    form_class = ClientTaskForm
    #template_name = 'task_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(ClientTaskUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Задачу'
       return context

    def get_form_kwargs(self):
       kwargs = super(ClientTaskUpdate, self).get_form_kwargs()
       kwargs.update({'user': self.request.user, 'action': 'update'})
       return kwargs       


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienttaskfilter(request):
    clientid = request.GET['clientid']
    taskstatus = request.GET['taskstatus']
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    #tskstatus_selectid = 0
    if taskstatus == "0":
       # если в выпадающем списке выбрано "Все активные"
       task_list = ClientTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid, dateclose__isnull=True)
    else:
       if taskstatus == "-1":
          # если в выпадающем списке выбрано "Все"
          task_list = ClientTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid)
       elif taskstatus == "-2":
          # если в выпадающем списке выбрано "Просроченные"
          task_list = ClientTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid, dateclose__isnull=True, dateend__lt=datetime.now())                         
       else:             
          task_list = ClientTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(client__members__in=[currentuser,]), is_active=True, client=clientid, status=taskstatus)
    # фильтр по принадлежности    
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
    return render(request, 'clients_list.html', {'nodes': nodes, 'object_list': 'clienttask_list', 'object_message': object_message}) 


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def clienttaskcomments(request, taskid):

    currenttask = ClientTask.objects.get(id=taskid)
    currentuser = request.user.id
    
    taskcomment_costsum = ClientTaskComment.objects.filter(task=taskid).aggregate(Sum('cost'))
    taskcomment_timesum = ClientTaskComment.objects.filter(task=taskid).aggregate(Sum('time'))
    try:
       sec = taskcomment_timesum["time__sum"]*3600
    except:
       sec = 0
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    seconds = sec
    taskcomment_list = ClientTaskComment.objects.filter(Q(author=request.user.id) | Q(task__client__members__in=[currentuser,]), is_active=True, task=taskid)
    #print(taskcomment_list)
    button_taskcomment_create = ''
    #button_taskcomment_update = ''
    button_task_create = ''
    button_task_update = ''    
    button_task_history = ''
    is_member = Client.objects.filter(members__in=[currentuser,]).exists()
    if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id or is_member:
       button_task_create = 'Добавить'
       button_task_history = 'История' 
       button_taskcomment_create = 'Добавить'             
       if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id:
          button_task_update = 'Изменить'
     
    return render(request, "clienttask_detail.html", {
                              'nodes': taskcomment_list.distinct().order_by(),
                              #'current_taskcomment': currenttaskcomment,
                              'clienttask': currenttask,
                              'button_clienttask_create': button_task_create,
                              'button_clienttask_update': button_task_update,
                              'button_clienttask_history': button_task_history,
                              #'object_list': 'clienttask_list',
                              'clienttaskcomment_costsum': taskcomment_costsum,
                              'clienttaskcomment_timesum': taskcomment_timesum,  
                              'hours': hours, 'minutes': minutes, 'seconds': seconds,                            
                              'button_clienttaskcomment_create': button_taskcomment_create,
                                                })      

class ClientTaskCommentDetail(DetailView):
    model = ClientTaskComment
    template_name = 'taskcomment_detail.html'

class ClientTaskCommentCreate(CreateView):    
    model = ClientTaskComment
    form_class = ClientTaskCommentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(ClientTaskCommentCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новый Комментарий'
       return context

    def form_valid(self, form):
       form.instance.task_id = self.kwargs['taskid']
       form.instance.author_id = self.request.user.id
       return super(ClientTaskCommentCreate, self).form_valid(form)

class ClientTaskCommentUpdate(UpdateView):    
    model = ClientTaskComment
    form_class = ClientTaskCommentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(ClientTaskCommentUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Комментарий'
       return context
