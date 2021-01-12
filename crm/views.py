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
#from projects.models import Dict_ProjectStatus, Dict_TaskStatus
#from projects.models import Project, Task, TaskComment, ProjectStatusLog, TaskStatusLog
from companies.forms import CompanyForm

from crm.models import Client, Dict_ClientStatus, Dict_ClientType
#from .forms import ProjectForm, TaskForm, TaskCommentForm
#from .forms import ProjectStatusLog, TaskStatusLog
from .forms import ClientForm #, ClientTaskForm, ClientTaskCommentForm

#from .tables import ProjectStatusLogTable, TaskStatusLogTable
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
             client_list = Client.objects.filter(Q(author=request.user.id) | Q(manager=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, status=prjstatus) #, dateclose__isnull=True)
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
    return render(request, "company_detail.html", {
                              'nodes': client_list.distinct().order_by(),
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
       context['header'] = 'Новый Проект'
       return context

    def get_form_kwargs(self):
       kwargs = super(ClientCreate, self).get_form_kwargs()
       # здесь нужно условие для 'action': 'create'
       kwargs.update({'user': self.request.user, 'action': 'create', 'companyid': self.kwargs['companyid']})
       return kwargs