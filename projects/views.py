from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import loader, Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist
#from versane.models import Company

from companies.models import Company
from projects.models import Project, Task, TaskComment, ProjectStatusLog, TaskStatusLog
from companies.forms import CompanyForm
from .forms import ProjectForm, TaskForm, TaskCommentForm
#from .utils import ObjectUpdateMixin

#class ProjectsHome(TemplateView):
#   template_name = 'home.html'

class ProjectsList(ListView):
    model = Project
    template_name = 'company_detail.html'

def projects(request, companyid, pk):

    if companyid == 0:
       companyid = request.session['_auth_user_currentcompany_id']
    
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
    button_company_select = 'Сменить организацию'
    # здесь нужно условие для button_company_create
    button_company_create = 'Добавить'
    # здесь нужно условие для button_company_update
    button_company_update = 'Изменить'
    # здесь нужно условие для button_project_create
    button_project_create = 'Добавить'

    return render(request, "company_detail.html", {
                              'nodes':Project.objects.all(),
                              'current_project':current_project,
                              'root_project_id':root_project_id,
                              'tree_project_id':tree_project_id,
                              'current_company':current_company,
                              'companyid':companyid,
                              'button_company_select': button_company_select,
                              'button_company_create': button_company_create,
                              'button_company_update': button_company_update,
                              'button_project_create': button_project_create,
                              #'task_id':task_id
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
       kwargs.update({'user': self.request.user, 'action': 'create'})
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

def tasks(request, projectid, pk):
    current_project = Project.objects.get(id=projectid)
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
#    try:
#       current_task = Task.objects.get(id=pk)
#    except ObjectDoesNotExist:
#       current_task = 0
#       tree_task_id = 0  
#       root_task_id = 0
#       tree_task_id = 0
#    else:   
#       tree_task_id = current_task.tree_id  
#       root_task_id = current_task.get_root().id
#       tree_task_id = current_task.tree_id


    button_project_create = ''
    button_project_update = ''
    button_task_create = ''
    # здесь нужно условие для button_project_create
    button_project_create = 'Добавить'
    # здесь нужно условие для button_project_update
    button_project_update = 'Изменить'
    # здесь нужно условие для button_task_create
    button_task_create = 'Добавить'
     
    return render(request, "project_detail.html", {
                              'nodes':Task.objects.all(),
                              'current_task':current_task,
                              'root_task_id':root_task_id,
                              'tree_task_id':tree_task_id,
                              'current_project':current_project,                             
                              'projectid':projectid,
                              'button_project_create': button_project_create,
                              'button_project_update': button_project_update,
                              'button_task_create': button_task_create,
                              #'taskcomment_id':taskcomment_id
                                                })       

class TaskDetail(DetailView):
   model = Task
   template_name = 'task_detail.html'  
    
   def get_context_data(self, **kwargs):
       context = super(TaskDetail, self).get_context_data(**kwargs)
       button_task_create = ''
       button_task_update = ''
       button_taskcomment_create = ''
       # здесь нужно условие для button_task_create
       button_task_create = 'Добавить'
       # здесь нужно условие для button_task_update
       button_task_update = 'Изменить'
       # здесь нужно условие для button_taskcomment_create
       button_taskcomment_create = 'Добавить'
       context['button_task_create'] = button_task_create
       context['button_task_update'] = button_task_update
       context['button_taskcomment_create'] = button_taskcomment_create
       #return super(TaskDetail, self).get_context_data(**kwargs)
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
       kwargs.update({'user': self.request.user, 'action': 'create'})
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
