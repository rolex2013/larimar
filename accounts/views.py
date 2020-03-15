from django.shortcuts import render, redirect, get_object_or_404

from urllib.parse import urlparse
 
#from django.shortcuts import redirect, render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView

from .forms import UserRegistrationForm

from companies.models import UserCompany

 
class ELoginView(View):
 
    def get(self, request):
        # если пользователь авторизован, то делаем редирект на главную страницу
        if auth.get_user(request).is_authenticated:
            return redirect('/')
        else:
            # Иначе формируем контекст с формой авторизации и отдаём страницу 
            # с этим контекстом.
            # работает, как для url - /admin/login/ так и для /accounts/login/ 
            context = create_context_username_csrf(request)
            #return render_to_response('accounts/login.html', context=context)
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
            request.session['_auth_user_company_id'] = '17'
            request.session.modified = True
            # ======================
            # получаем предыдущий url
            #next = urlparse(get_next_url(request)).path
            next = '/projects/'
            # и если пользователь из числа персонала и заходил через url /admin/login/
            # то перенаправляем пользователя в админ панель
            if next == '/admin/login/' and request.user.is_staff:
                return redirect('/admin/')
            # иначе делаем редирект на предыдущую страницу,
            # в случае с /accounts/login/ произойдёт ещё один редирект на главную страницу
            # в случае любого другого url, пользователь вернётся на данный url
            return redirect(next)
 
        # если данные не верны, то пользователь окажется на странице авторизации
        # и увидит сообщение об ошибке
        context = create_context_username_csrf(request)
        context['login_form'] = form
 
        #return render_to_response('accounts/login.html', context=context)
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
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})