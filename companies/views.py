from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime, date, time
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import loader, Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist

from .models import Company, UserCompanyComponentGroup, Content, Dict_ContentType
#from projects.models import Project, Task, TaskComment
from .forms import CompanyForm, ContentForm

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
            #button_company_select = 'Сменить организацию'
            context['user_companies'] = self.request.session['_auth_user_companies_id']
            #context['button_company_select'] = button_company_select
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

    # здесь нужно условие для button_company_create
    button_company_create = ''
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

       if form.is_valid():
          org = form.save()
          UserCompanyComponentGroup.objects.create(user_id=form.instance.author_id, 
                                                   company_id=org.id,
                                                   component_id=5,
                                                   group_id=1)

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

def contents(request):
    template_name = 'home.html'
    companies_id = request.session['_auth_user_companies_id']
    content_list = Content.objects.filter(is_active=True, datebegin__lte=datetime.now(), dateend__gte=datetime.now(), company_id__in=companies_id)
    # здесь нужно условие для button_company_create
    button_content_create = ''
    # if юзер имеет право на добавление контента
    #     button_content_create = 'Добавить'
    
    return render(request, template_name, {
                              'content_list': content_list,
                              'user_companies': request.session['_auth_user_companies_id'],
                              'button_content_create': button_content_create,                              
                                            })  

class ContentList(ListView):
    model = Content
    #template_name = 'content.html' 
    template_name = 'home.html'
    #ordering = ['company_up', 'id']

    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            #current_membership = get_user_membership(self.request)
            #context['current_membership'] = str(current_membership.membership)
            # добавляем к контексту сессионный массив с id компаний, доступными этому авторизованному юзеру
            #button_company_select = 'Сменить организацию'
            context['user_companies'] = self.request.session['_auth_user_companies_id']
            #context['button_company_select'] = button_company_select
            return context

class ContentDetail(DetailView):
    model = Content
    template_name = 'content_detail.html' 

    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['user_companies'] = self.request.session['_auth_user_companies_id']
            return context    

class ContentCreate(CreateView):    
    model = Content
    form_class = ContentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(ContentCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новый Контент'
       return context

    def form_valid(self, form):
       #form.instance.company_id = self.kwargs['companyid']
       form.instance.author_id = self.request.user.id
       return super(ContentCreate, self).form_valid(form)

class ContentUpdate(UpdateView):    
    model = Content
    form_class = ContentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(ContentUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Контент'
       return context
