from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import loader, Context, RequestContext
#from versane.models import Company

from .models import Company, Project, Task, TaskComment
from .forms import CompanyForm, ProjectForm, TaskForm, TaskCommentForm
#from .utils import ObjectUpdateMixin

class ProjectsHome(TemplateView):
   template_name = 'home.html'

class CompaniesList(ListView):
    model = Company
    template_name = 'menu_companies.html' 
    #ordering = ['company_up', 'id']

def companies(request, pk):
    current_company = Company.objects.get(id=pk)
    root_company_id = current_company.get_root().id
    tree_company_id = current_company.tree_id

    try:  
       current_project = current_company.resultcompany.all()[0].id
    except (ValueError, IndexError) as e:
       project_id = 0
    else:
       project_id = 0 #current_project

    return render(request, "companies.html", {
                              'nodes':Company.objects.all(),
                              'current_company':current_company,
                              'root_company_id':root_company_id,
                              'tree_company_id':tree_company_id,
                              'project_id':project_id
                                            })  

def tree_get_root(request, pk):
    current_company = Company.objects.get(id=pk)
    root_company_id = current_company.get_root().id
    return root_company_id                                                                            

class CompanyDetail(DetailView):
    model = Company
    template_name = 'company_detail.html'

class CompanyCreate(CreateView):    
    model = Company
    form_class = CompanyForm
    #template_name = 'project_create.html'
    template_name = 'object_form.html'

    def form_valid(self, form):
       form.instance.author_id = self.request.user.id
       form.instance.parent_id = self.kwargs['parentid']
       return super(CompanyCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(CompanyCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новая Организация'
       return context

class CompanyUpdate(UpdateView):    
    model = Company
    form_class = CompanyForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(CompanyUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Организацию'
       return context


class ProjectsList(ListView):
    model = Project
    template_name = 'company_detail.html'

def projects(request, companyid, pk):
    current_company = Company.objects.get(id=companyid)
    current_project = Project.objects.get(id=pk)
    tree_project_id = current_project.tree_id  
    root_project_id = current_project.get_root().id
    tree_project_id = current_project.tree_id
    try:  
       current_task = current_project.resultproject.all()[0].id
    except (ValueError, IndexError) as e:
       task_id = 0
    else:
       task_id = current_task
    return render(request, "company_detail.html", {
                              'nodes':Project.objects.all(),
                              'current_project':current_project,
                              'root_project_id':root_project_id,
                              'tree_project_id':tree_project_id,
                              'current_company':current_company,
                              'companyid':companyid,
                              'task_id':task_id
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
       form.instance.author_id = self.request.user.id
       form.instance.company_id = self.kwargs['companyid']
       form.instance.parent_id = self.kwargs['parentid']
       return super(ProjectCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(ProjectCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новый Проект'
       return context

class ProjectUpdate(UpdateView):    
    model = Project
    form_class = ProjectForm
    #template_name = 'project_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(ProjectUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Проект'
       return context

#class ProjectDelete(DeleteView):    
#    model = Project
#    #form_class = ProjectForm
#    template_name = 'project_delete.html'
#    success_url = '/success/' 

def tasks(request, projectid, pk):
    current_project = Project.objects.get(id=projectid)
    current_task = Task.objects.get(id=pk)
    tree_task_id = current_task.tree_id  
    root_task_id = current_task.get_root().id
    tree_task_id = current_task.tree_id
    #try:  
    #   current_comment = current_task.resulttask.all()[0].id
    #except (ValueError, IndexError) as e:
    #   taskcomment_id = 0
    #else:
    #   taskcomment_id = current_comment    
    return render(request, "project_detail.html", {
                              'nodes':Task.objects.all(),
                              'current_task':current_task,
                              'root_task_id':root_task_id,
                              'tree_task_id':tree_task_id,
                              'current_project':current_project,                             
                              'projectid':projectid,
                              #'taskcomment_id':taskcomment_id
                                                })       


class TaskDetail(DetailView):
    model = Task
    template_name = 'task_detail.html'  
    
    #def index(request):
    #   data = {"Filter_1": user.is_authenticated and taskcomment.is_active, "message": "Welcome to Python"}
    #   return render(request, "task_detail.html", context=data)

class TaskCreate(CreateView):    
    model = Task
    form_class = TaskForm
    #template_name = 'task_create.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(TaskCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новая Задача'
       return context

    def form_valid(self, form):
       form.instance.parent_id = self.kwargs['parentid']
       form.instance.project_id = self.kwargs['projectid']
       form.instance.author_id = self.request.user.id
       return super(TaskCreate, self).form_valid(form)

class TaskUpdate(UpdateView):    
    model = Task
    form_class = TaskForm
    #template_name = 'task_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(TaskUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Задачу'
       return context    

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
