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
    #getting detail information about current object
    current_company = Company.objects.get(id=pk)
    root_company_id = current_company.get_root().id
    #render
    #return render("companies.html",
    #                      {
    #                          'nodes':Company.objects.all(),
    #                          'current_company':current_company,
    #                          'root_company_id':root_company_id
    #                      },
    #                      context_instance=RequestContext(request))    
    return render(request, "companies.html", {
                              'nodes':Company.objects.all(),
                              'current_company':current_company,
                              'root_company_id':root_company_id
                                                    })                          

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
       form.instance.parent_id = self.kwargs['companyid']
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
       #form.instance.parent_id = self.kwargs['projectid']
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
       form.instance.parent_id = self.kwargs['taskid']
       #form.instance.project_id = self.kwargs['projectid']
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
