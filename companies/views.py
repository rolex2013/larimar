from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import loader, Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist

from .models import Company
from projects.models import Project, Task, TaskComment
from .forms import CompanyForm

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
       project_id = current_project

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
       if self.kwargs['parentid'] != 0:
          form.instance.parent_id = self.kwargs['parentid']
       #else:
       #   form.instance.parent_id = form.instance.id
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
