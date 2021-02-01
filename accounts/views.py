from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, time

from urllib.parse import urlparse

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
 
#from django.shortcuts import redirect, render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
#from django.core import serializers

from .forms import UserRegistrationForm, UserProfileForm

from main.models import Notification, Meta_ObjectType
#from .tables import NotificationTable
from companies.models import UserCompanyComponentGroup, Content
from .models import UserProfile
from django.db.models import Count

#from companies.views import publiccontents

 
class ELoginView(View):
 
    def get(self, request):
        # если пользователь авторизован, то делаем редирект на главную страницу
        if auth.get_user(request).is_authenticated:
            return redirect('/')
        else:
            # Иначе формируем контекст с формой авторизации и отдаём страницу 
            # с этим контекстом.
            # работает, как для url - /admin/login/ так и для /account/login/ 
            context = create_context_username_csrf(request)
            #return render_to_response('account/login.html', context=context)
            return render(request, 'registration/login.html', context=context)
 
    def post(self, request):
        # получив запрос на авторизацию
        form = AuthenticationForm(request, data=request.POST)
 
        # проверяем правильность формы, что есть такой пользователь
        # и он ввёл правильный пароль
        if form.is_valid():
            # в случае успеха авторизуем пользователя
            auth.login(request, form.get_user())
            # ======================
            # получаем список организаций, привязанных к этому пользователю из companies.UserCompany
            # хорошо бы этот список сделать глобальным для всех приложений
            #uc = getVariables(request)
            #companies_list = request.UserCompany.objects.get(user=request.user)
            #uc['UserCompany'] = companies_list
            #companies_list = UserCompany.objects.filter(user=request.user.id, is_active=True).only('company')
            current_company = ''
            # === проверяем существование профиля ===
            try:
               current_profile = UserProfile.objects.get(user=request.user.id, is_active=True)
            except ObjectDoesNotExist:
               UserProfile.objects.create(user_id=request.user.id, description='')
            # === проверяем, есть ли в настройках профиля какая-нибудь Организация ===
            current_company = UserProfile.objects.get(user=request.user.id, is_active=True).company_id
            if current_company == None:
               # === проверяем, даны ли права этому пользователю на какую-нибудь Организацию ===
               current_company = list(UserCompanyComponentGroup.objects.filter(user=request.user.id, is_active=True).values_list("company", flat=True))[0]
               if current_company != None:
                  UserProfile.objects.filter(user_id=request.user.id).update(company_id=current_company)               
            # ========================================         
            #print(current_company)
            request.session['_auth_user_currentcompany_id'] = current_company
            companies_list = list(UserCompanyComponentGroup.objects.filter(user=request.user.id, is_active=True).values_list("company", flat=True))
            request.session['_auth_user_companies_id'] = companies_list
            components_list = list(UserCompanyComponentGroup.objects.filter(user=request.user.id, is_active=True).values_list("component", flat=True))         
            request.session['_auth_user_component_id'] = components_list
            usergroups_list = list(UserCompanyComponentGroup.objects.filter(user=request.user.id, is_active=True).values_list("group", flat=True))            
            request.session['_auth_user_group_id'] = usergroups_list
            request.session.modified = True
            # ======================
            # получаем предыдущий url
            #next = urlparse(get_next_url(request)).path
            #next = '/projects/main/'
            next = '/main/'
            # и если пользователь из числа персонала и заходил через url /admin/login/
            # то перенаправляем пользователя в админ панель
            if next == '/admin/login/' and request.user.is_staff:
                return redirect('/admin/')
            # иначе делаем редирект на предыдущую страницу,
            # в случае с /account/login/ произойдёт ещё один редирект на главную страницу
            # в случае любого другого url, пользователь вернётся на данный url
            return redirect(next)
 
        # если данные не верны, то пользователь окажется на странице авторизации
        # и увидит сообщение об ошибке
        context = create_context_username_csrf(request)
        context['login_form'] = form
 
        #return render_to_response('account/login.html', context=context)
        return render(request, 'registration/login.html', context=context)
 
 
# вспомогательный метод для формирования контекста с csrf_token
# и добавлением формы авторизации в этом контексте
def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context['login_form'] = AuthenticationForm
    return context


class ELogoutView(LogoutView):  
    template_name = 'registration/logout.html'
    #pbcontent = publiccontents
    #template_name = 'index.html' 

# эта ф-ция после логаута переадресовывает на начальную страницу с публичным контентом (внешний сайт)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            #print(new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

#
#class UserProfileDetail(DetailView):
#    model = UserProfile
#    template_name = 'userprofile_detail.html'    
#
#    def get_queryset(self):
#        return UserProfile.objects.filter(user_id=self.request.user.id) #self.kwargs['userid'])
#

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def UserProfileDetail(request, userid=0, param=''):

    companies_id = request.session['_auth_user_companies_id']
    if userid == 0:
       userid = request.user.id 
       if param == 'all':
          #content_list = Content.objects.filter(author_id=userid, is_forprofile=True).annotate(cnt=Count('id'))          
          #content_list = Content.objects.filter(author_id=userid, place_id=3).annotate(cnt=Count('id'))  
          content_list = Content.objects.filter(author_id=userid).annotate(cnt=Count('id'))        
       else:
          content_list = Content.objects.filter(author_id=userid, is_active=True, datebegin__lte=datetime.now(), dateend__gte=datetime.now(), place_id=3).annotate(cnt=Count('id'))
    else:
       content_list = Content.objects.filter(author_id=userid, is_active=True, datebegin__lte=datetime.now(), dateend__gte=datetime.now(), place_id=3).annotate(cnt=Count('id'))          
    user_profile = UserProfile.objects.get(user=userid, is_active=True) #.company_id

    notification_list = Notification.objects.filter(recipient_id=userid, is_active=True, is_read=False, type_id=3)
    #table = NotificationTable(notification_list)
    metaobjecttype_list = Meta_ObjectType.objects.filter(is_active=True)

    #button_project_create = ''
    button_userprofile_update = 'Изменить'
    prompt_is_notify = 'Вкл.'
    if user_profile.is_notify == False:
       prompt_is_notify = 'Выкл.'

    return render(request, 'userprofile_detail.html', {
                                                       'user_profile': user_profile,
                                                       'button_userprofile_update': button_userprofile_update,
                                                       'content_list': content_list,
                                                       'user_companies': companies_id,
                                                       'prompt_is_notify': prompt_is_notify,
                                                       'notification_list': notification_list.distinct().order_by("-datecreate"),
                                                       'metaobjecttype_list': metaobjecttype_list.distinct().order_by(),
                                                       'status_selectid': '2',
                                                       'metaobjecttype_selectid': '0',                                                       
                                                       #'table': table,
                                                      })


class UserProfileUpdate(UpdateView):    
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'object_form.html'
    #success_url = '../3'

    def get_context_data(self, **kwargs):
       context = super(UserProfileUpdate, self).get_context_data(**kwargs)
       context['header'] = 'Изменить Профиль'
       return context

    def get_form_kwargs(self):
       kwargs = super(UserProfileUpdate, self).get_form_kwargs()
       # здесь нужно условие для 'action': 'update'
       kwargs.update({'org': self.request.session['_auth_user_companies_id']})
       return kwargs

    # записываем новое значение текущей компании из профиля в переменную сессии
    def form_valid(self, form):
        #form.instance.user = self.request.user
        form.save()
        current_company = UserProfile.objects.get(user=self.request.user.id, is_active=True).company_id
        self.request.session['_auth_user_currentcompany_id'] = current_company
        return super(UserProfileUpdate, self).form_valid(form)
                 