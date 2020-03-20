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

    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            #current_membership = get_user_membership(self.request)
            #context['current_membership'] = str(current_membership.membership)
            # добавляем к контексту сессионный массив с id компаний, доступными этому авторизованному юзеру
            context['user_companies'] = self.request.session['_auth_user_companies_id']
            return context

#def companies_main(request):
#    companies_list = Company.objects.filter(is_active=True)
#    #companies_list = Company.objects.all()
#    return render(request, 'menu_companies.html', {
#                              'node': companies_list, #Company.objects.all(),
#                              'user_companies': request.session['_auth_user_companies_id'],
#                                             }
#                 )  

def companies(request, pk):
    #current_company = Company.objects.get(id=pk)
    #root_company_id = current_company.get_root().id
    #tree_company_id = current_company.tree_id
 
    #try:  
    #   current_project = current_company.resultcompany.all()[0].id
    #except (ValueError, IndexError) as e:
    #   project_id = 0
    #else:
    #   project_id = current_project

    #if pk == 0:
    #   current_company_id = request.session['_auth_user_companies_id']
    #   pk = current_company_id[0]

    if pk == 0:
       current_company = 0
       tree_company_id = 0
       root_company_id = 0
       tree_company_id = 0
       project_id = 0
       template_name = "menu_companies.html"
       #template_name = "companies.html"
    else:
       current_company = Company.objects.get(id=pk)
       tree_company_id = current_company.tree_id  
       root_company_id = current_company.get_root().id
       tree_company_id = current_company.tree_id
       template_name = "companies.html"
       try:  
          current_project = current_company.resultcompany.all()[0].id
       except (ValueError, IndexError) as e:
          project_id = 0
       else:
          project_id = current_project       

    #if 
    button_company_create = 'Добавить'

    return render(request, template_name, {
                              'nodes':Company.objects.all(),
                              'current_company':current_company,
                              'root_company_id':root_company_id,
                              'tree_company_id':tree_company_id,
                              'project_id':project_id,
                              'user_companies': request.session['_auth_user_companies_id'],
                              'button_company_create': button_company_create,
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