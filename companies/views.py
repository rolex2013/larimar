from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import loader, Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist

from .models import Company, UserCompany
from projects.models import Project, Task, TaskComment
from .forms import CompanyForm

class CompaniesList(ListView):
    model = Company
    template_name = 'menu_companies.html' 
    #ordering = ['company_up', 'id']

def companies(request, pk):
    current_company = Company.objects.get(id=pk)
    #user_companies = UserCompany.objects.get(user=request.user)
    root_company_id = current_company.get_root().id
    tree_company_id = current_company.tree_id

    #all_root_items = Company.objects.filter(is_active=1,id=pk).order_by('tree_id', 'lft')
    ##all_root_items = Company.objects.all()
    #companies_list = []
    #for item in all_root_items:
    #   #usr = UserCompany.objects.filter(company=item)
    #   companies_list.append({'id': item.id, 'name': item.name, 'parent_id': item.parent_id, 
    #      'description': item.description, 'structure_type_id': item.structure_type, 'type_id': item.type,
    #      'datecreate': item.datecreate, 'author_id': item.author_id, 'is_active': item.is_active,
    #      'tree_id': item.tree_id, 'lft': item.lft, 'rght': item.rght, 'level': item.level})
    
    #companies_list = list(Company.objects.order_by('tree_id', 'lft'))
    #for i, obj in enumerate(companies_list):
    #   obj.myIntB = i
    #   usr = UserCompany.objects.filter(company=companies_list['company'])
    #   #companies_list[i]['user'] = usr
    #   obj.user = usr

    enriched_models = []
    companies_list = Company.objects.all()
    for i in companies_list:
        enriched_models.append((i, 'user'))       

    try:  
       current_project = current_company.resultcompany.all()[0].id
    except (ValueError, IndexError) as e:
       project_id = 0
    else:
       project_id = current_project

    return render(request, "companies.html", {
                              #'nodes':Company.objects.all(),
                              'nodes': companies_list,
                              "UserCompany": enriched_models,
                              'current_company':current_company,
                              'root_company_id':root_company_id,
                              'tree_company_id':tree_company_id,
                              'project_id':project_id,
                              #'uc':UserCompany.objects.filter(user=request.user),
                              #'usr':usr,
                              'user_company': request.session['_auth_user_company_id'],
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

#def getCompanies(request, user):
#    #uc = UserCompany.objects.get(user=user)
#    return render(request, "menu_companies.html", {'nodes':request.UserCompany.objects.get(user=user)})