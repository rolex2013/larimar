from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime, date, time
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.template import loader, Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.db.models import Q

from .models import Company, UserCompanyComponentGroup, StaffList, Content, Dict_ContentType, Dict_ContentPlace
#from projects.models import Project, Task, TaskComment
from .forms import CompanyForm, StaffListForm, ContentForm

#class CompaniesList(ListView):
#    model = Company
#    template_name = 'menu_companies.html' 
#    #ordering = ['company_up', 'id']
#
#    def get_context_data(self, *args, **kwargs):
#        if self.request.user.is_authenticated:
#            context = super().get_context_data(**kwargs)
#            #current_membership = get_user_membership(self.request)
#            #context['current_membership'] = str(current_membership.membership)
#            # добавляем к контексту сессионный массив с id компаний, доступными этому авторизованному юзеру
#            #button_company_select = 'Сменить организацию'
#            context['user_companies'] = self.request.session['_auth_user_companies_id']
#            #context['button_company_select'] = button_company_select
#            return context

#def companies_main(request):
#    companies_list = Company.objects.filter(is_active=True)
#    #companies_list = Company.objects.all()
#    return render(request, 'menu_companies.html', {
#                              'node': companies_list, #Company.objects.all(),
#                              'user_companies': request.session['_auth_user_companies_id'],
#                                             }
#                 )  

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def companies(request, pk=0):

    comps = request.session['_auth_user_companies_id']
    if pk == 0:
       current_company = 0
       tree_company_id = 0
       root_company_id = 0
       tree_company_id = 0
       project_id = 0
       #template_name = "menu_companies.html"
       template_name = "companies.html"
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
    button_StaffList = "Штатное расписание"
    
    return render(request, template_name, {
                              #'nodes':Company.objects.all(),
                              'nodes': Company.objects.filter(is_active=True, id__in=comps).order_by(),
                              'current_company': current_company,
                              'root_company_id': root_company_id,
                              'tree_company_id': tree_company_id,
                              'project_id': project_id,
                              'user_companies': comps, #request.session['_auth_user_companies_id'],
                              'button_company_create': button_company_create,
                              'button_StaffList': button_StaffList,
                              'object_list': 'company_list',                              
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

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def stafflist(request, companyid=0, pk=0):

    if companyid == 0:
       companyid = request.session['_auth_user_currentcompany_id']

    comps = request.session['_auth_user_companies_id']
    current_company = Company.objects.get(id=companyid)

    if pk == 0:
       current_stafflist = 0
       tree_stafflist_id = 0
       root_stafflist_id = 0
       tree_stafflist_id = 0
       stafflist_id = 0
       #template_name = "stafflist.html"
    else:
       current_stafflist = StaffList.objects.get(id=pk)
       tree_stafflist_id = current_stafflist.tree_id  
       root_stafflist_id = current_stafflist.get_root().id
       tree_stafflist_id = current_stafflist.tree_id
    template_name = "company_detail.html"

    # здесь нужно условие для button_stafflist_create
    button_stafflist_create = ''
    button_stafflist_create = 'Добавить'
    #button_stafflist = "Штатное расписание"
    
    return render(request, template_name, {
                              'nodes': StaffList.objects.filter(is_active=True, company_id=companyid).order_by(),
                              'current_stafflist': current_stafflist,
                              'root_stafflist_id': root_stafflist_id,
                              'tree_stafflist_id': tree_stafflist_id,
                              'current_company': current_company,
                              'companyid': companyid,
                              'user_companies': comps,                              
                              'button_stafflist_create': button_stafflist_create,
                              #'button_StaffList': button_stafflist,
                              'object_list': 'stafflist_list',                              
                                            })

#class StaffListDetail(DetailView):
#    model = StaffList
#    template_name = 'stafflist_detail.html'

class StaffListCreate(CreateView):    
    model = StaffList
    form_class = StaffListForm
    template_name = 'object_form.html'

    def form_valid(self, form):
       form.instance.author_id = self.request.user.id
       if self.kwargs['parentid'] != 0:
          form.instance.parent_id = self.kwargs['parentid']

       #if form.is_valid():
       #   org = form.save()
       #   UserCompanyComponentGroup.objects.create(user_id=form.instance.author_id, 
       #                                            company_id=org.id,
       #                                            component_id=5,
       #                                            group_id=1)

       return super(StaffListCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(StaffListCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новая Должность'
       return context

class StaffListUpdate(UpdateView):    
    model = StaffList
    form_class = StaffListForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(StaffListUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Должность'
       return context


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def contents(request, place=0):
    template_name = 'main.html'
    if place == 1:
       template_name = 'userprofile_detail.html'

    #if user.is_authenticated:
    companies_id = request.session['_auth_user_companies_id']
    content_list = ''
    if request.user.is_authenticated:
       #content_list = Content.objects.filter(is_active=True, datebegin__lte=datetime.now(), dateend__gte=datetime.now(), company__is_active=True, company_id__in=companies_id)
       #result=list(set(companies_id) & set(Word)) # - пример пересечения множеств
       if place == 0:
          content_list = Content.objects.filter(is_active=True, datebegin__lte=datetime.now(), dateend__gte=datetime.now(), company__is_active=True, company__in=companies_id, place_id=2).annotate(cnt=Count('id'))
       else:
          content_list = Content.objects.filter(is_active=True, datebegin__lte=datetime.now(), dateend__gte=datetime.now(), company__is_active=True, company__in=companies_id, place_id=3).annotate(cnt=Count('id'))          
                      # это надо как-то исправить, чтоб записи не дублировались, когда контент для нескольких компаний, и они же есть в списке у пользователя!
     # здесь нужно условие для button_company_create
     # юзер имеет право на добавление контента
     # это реализовано в шаблоне через штатный perms.companies.add_content
    button_content_create = ''
    #is_add2 = 'SELECT p.id FROM auth_user_groups ug INNER JOIN auth_user u ON u.id=ug.user_id INNER JOIN auth_group_permissions gp ON gp.group_id=ug.group_id INNER JOIN auth_permission p ON p.id=gp.permission_id WHERE u.is_superuser OR (ug.user_id=2 AND p.codename="add_content")'
    #is_add1 = 'SELECT p.id FROM auth_user_user_permissions uup INNER JOIN auth_permission p ON p.id=uup.permission_id WHERE uup.user_id=3 AND p.codename="add_content"'
    #is_add.query = auth_user_user_permissions.objects.filter(user_id=3, auth_permission__codename='add_content').values('auth_permission__id')
    #u = User.objects.add_content(username='larimarit')
    #is_add = u.has_perm('add_content')
    #if is_add:
    #   button_content_create = 'Добавить'
    #else:
    #   if is_add2:
    #      button_content_create = 'Добавить'
   
    return render(request, template_name, {
                              'content_list': content_list,
                              'user_companies': companies_id, #request.session['_auth_user_companies_id'],
                              'button_content_create': button_content_create,                              
                                            })  

def publiccontents(request):
    template_name = 'index.html'

    #content_list = Content.objects.filter(is_active=True, datebegin__lte=datetime.now(), dateend__gte=datetime.now(), company__is_active=True, is_public=True, is_forprofile=False, is_private=False).annotate(cnt=Count('id'))
    content_list = Content.objects.filter(is_active=True, datebegin__lte=datetime.now(), dateend__gte=datetime.now(), company__is_active=True, place__is_active=True, place_id=1).annotate(cnt=Count('id')) 
    #print('***********************')
    return render(request, template_name, {
                              'content_list': content_list,                              
                                            })

class ContentList(ListView):
    model = Content
    #template_name = 'content.html' 
    template_name = 'main.html'
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

    def get_object(self):
        object = super(ContentDetail, self).get_object()
        if not self.request.user.is_authenticated and object.is_public == False:
           raise Http404
        return object

    def get_context_data(self, *args, **kwargs):
       context = super(ContentDetail, self).get_context_data(**kwargs)
       #print(self.object.name)       
       if self.request.user.is_authenticated:
          context['button_content_create'] = 'Добавить' #button_company_create
          context['button_content_update'] = 'Изменить'
          context['user_companies'] = self.request.session['_auth_user_companies_id']
          context['whoisauthor'] = 'Автор: ' + self.object.author.username
          if not self.object.is_active:
             context['extdescription'] = ' (Контент перемещен в архив)'
          return context              
       elif self.object.is_public == True:
          return context  
       #context['extdescription'] = ' Контент недоступен!'

class ContentCreate(CreateView):    
    model = Content
    form_class = ContentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
       context = super(ContentCreate, self).get_context_data(**kwargs)
       context['header'] = 'Новый Контент'
       return context

    def get_form_kwargs(self):
       kwargs = super(ContentCreate, self).get_form_kwargs()
       # здесь нужно условие для 'action': 'create'
       kwargs.update({'org': self.request.session['_auth_user_companies_id']})
       return kwargs

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

    def get_form_kwargs(self):
       kwargs = super(ContentUpdate, self).get_form_kwargs()
       # здесь нужно условие для 'action': 'update'
       kwargs.update({'org': self.request.session['_auth_user_companies_id']})
       return kwargs

