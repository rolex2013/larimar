from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, date, time

from urllib.parse import urlparse

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotFound,
)

# from django.shortcuts import redirect, render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView

# from django.core import serializers

from .forms import UserRegistrationForm, UserInviteForm, UserAddForm, UserProfileForm

from main.models import Component, Notification, Meta_ObjectType

# from .tables import NotificationTable
from companies.models import Company, UserCompanyComponentGroup, Content
from feedback.models import Dict_System
from .models import UserProfile
from django.db.models import Count

import sys
import pytz

import requests
from bs4 import BeautifulSoup as BS
from time import sleep

# from companies.views import publiccontents


class ELoginView(View):
    def get(self, request):
        # если пользователь авторизован, то делаем редирект на главную страницу
        # if auth.get_user(request).is_authenticated:
        #    return redirect('/')
        # else:
        # Иначе формируем контекст с формой авторизации и отдаём страницу
        # с этим контекстом.
        # работает, как для url - /admin/login/ так и для /account/login/
        context = create_context_username_csrf(request)
        # return render_to_response('account/login.html', context=context)
        return render(request, "registration/login.html", context=context)

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
            # uc = getVariables(request)
            # companies_list = request.UserCompany.objects.get(user=request.user)
            # uc['UserCompany'] = companies_list
            # companies_list = UserCompany.objects.filter(user=request.user.id, is_active=True).only('company')
            current_company = ""
            # === проверяем существование профиля ===
            try:
                current_profile = UserProfile.objects.get(
                    user=request.user.id, is_active=True
                )
            except ObjectDoesNotExist:
                UserProfile.objects.create(user_id=request.user.id, description="")
            # === проверяем, есть ли в настройках профиля какая-нибудь Организация ===
            current_company = UserProfile.objects.get(
                user=request.user.id, is_active=True
            ).company_id
            if current_company == None:
                # === проверяем, даны ли права этому пользователю на какую-нибудь Организацию ===
                try:
                    current_company = list(
                        UserCompanyComponentGroup.objects.filter(
                            user=request.user.id, is_active=True
                        ).values_list("company", flat=True)
                    )[0]
                except:
                    if sys.platform == "win32":
                        cmp_id = 7
                    else:
                        cmp_id = 1
                    # cmp_id=''
                    if request.user.is_superuser == True:
                        UserCompanyComponentGroup.objects.create(
                            user_id=request.user.id,
                            company_id=cmp_id,
                            component_id=1,
                            group_id=1,
                        )
                    else:
                        UserCompanyComponentGroup.objects.create(
                            user_id=request.user.id,
                            company_id=cmp_id,
                            component_id=1,
                            group_id=8,
                        )
                current_company = list(
                    UserCompanyComponentGroup.objects.filter(
                        user=request.user.id, is_active=True
                    ).values_list("company", flat=True)
                )[0]
                if current_company != None:
                    UserProfile.objects.filter(user_id=request.user.id).update(
                        company_id=current_company
                    )
            # ========================================
            # print(current_company)
            # *** проверяем, является ли эта система системой разработчика 1YES!
            try:
                systemdev = Dict_System.objects.filter(
                    is_active=True, code="1YES-1YES-1YES-1YES"
                ).first()
                systemdevid = systemdev.id
                is_system_dev = systemdev.is_local
            except:
                systemdevid = 2
                is_system_dev = False
            request.session["system_dev"] = (systemdevid, is_system_dev)
            # ***
            request.session["_auth_user_currentcompany_id"] = current_company
            companies_list = list(
                UserCompanyComponentGroup.objects.filter(
                    user=request.user.id, is_active=True
                ).values_list("company", flat=True)
            )
            request.session["_auth_user_companies_id"] = list(set(companies_list))
            usergroups_list = list(
                UserCompanyComponentGroup.objects.filter(
                    user=request.user.id, is_active=True
                ).values_list("group", flat=True)
            )
            request.session["_auth_user_group_id"] = list(set(usergroups_list))
            if 1 in request.session["_auth_user_group_id"]:
                components_list = list(
                    Component.objects.filter(is_active=True).values_list(
                        "id", flat=True
                    )
                )
            else:
                components_list = list(
                    UserCompanyComponentGroup.objects.filter(
                        user=request.user.id, is_active=True
                    ).values_list("component", flat=True)
                )
                # print(current_company)
            request.session["_auth_user_component_id"] = list(set(components_list))
            request.session[settings.LANGUAGE_COOKIE_NAME] = current_profile.lang
            request.session.modified = True
            # ======================
            # получаем предыдущий url
            # next = urlparse(get_next_url(request)).path
            # next = '/projects/main/' # 0,1,0,1,1,1,1,1,0,0,1
            next = "/main/"
            # и если пользователь из числа персонала и заходил через url /admin/login/
            # то перенаправляем пользователя в админ панель
            if next == "/admin/login/" and request.user.is_staff:
                return redirect("/admin/")
            # иначе делаем редирект на предыдущую страницу,
            # в случае с /account/login/ произойдёт ещё один редирект на главную страницу
            # в случае любого другого url, пользователь вернётся на данный url
            return redirect(next)

        # если данные не верны, то пользователь окажется на странице авторизации
        # и увидит сообщение об ошибке
        context = create_context_username_csrf(request)
        context["login_form"] = form

        # return render_to_response('account/login.html', context=context)
        return render(request, "registration/login.html", context=context)


# вспомогательный метод для формирования контекста с csrf_token
# и добавлением формы авторизации в этом контексте
def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context["login_form"] = AuthenticationForm
    return context


class ELogoutView(LogoutView):
    template_name = "registration/logout.html"
    # pbcontent = publiccontents
    # template_name = 'index.html'


# эта ф-ция после логаута переадресовывает на начальную страницу с публичным контентом (внешний сайт)
def logout_view(request):
    del request.session["websocket_test"]
    logout(request)
    return HttpResponseRedirect("/")


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            if request.recaptcha_is_valid:
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data["password"])
                # Save the User object
                new_user.save()
                if user_form.cleaned_data["is_org_register"] == True:
                    instance_comp = Company.objects.create(
                        name="Ваша новая Компания",
                        description="Создана автоматически при регистрации пользователя",
                        is_active=1,
                        lft=1,
                        rght=1,
                        tree_id=1,
                        level=0,
                        structure_type_id=1,
                        type_id=4,
                        currency_id=1,
                        author_id=new_user.id,
                    )
                    UserProfile.objects.create(
                        user_id=new_user.id,
                        company_id=instance_comp.id,
                        is_notify=True,
                        protocoltype_id=3,
                        description="Профиль создан автоматически при регистрации пользователя",
                    )
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.id,
                        company_id=instance_comp.id,
                        component_id=1,
                        group_id=2,
                    )
                else:
                    # регистрируется в качестве Гостя первой зарегистрированной Организации
                    comp_id = Company.objects.all()[0].id
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.id,
                        company_id=comp_id,
                        component_id=1,
                        group_id=8,
                    )
                return render(
                    request,
                    "registration/register_done.html",
                    {
                        "new_user": new_user,
                        "companyid": "0",
                    },
                )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        "registration/register.html",
        {
            "user_form": user_form,
            "param": "register",
        },
    )


def add(request, companyid=1):
    if request.method == "POST":
        user_form = UserAddForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            upr = UserProfile.objects.filter(user_id=new_user.user.id).first()
            if upr == None:
                UserProfile.objects.create(
                    user_id=new_user.user.id,
                    company_id=companyid,
                    is_notify=True,
                    protocoltype_id=1,
                    description="Профиль создан Администратором Организации",
                )
            if user_form["is_staff"].value() == True:
                # для Сотрудника
                try:
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=1,
                        group_id=7,
                    )
                except:
                    UserCompanyComponentGroup.objects.filter(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=1,
                        group_id=7,
                        is_active=False,
                    ).update(is_active=True)
                try:
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=5,
                        group_id=7,
                    )
                except:
                    UserCompanyComponentGroup.objects.filter(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=5,
                        group_id=7,
                        is_active=False,
                    ).update(is_active=True)
                try:
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=6,
                        group_id=7,
                    )
                except:
                    UserCompanyComponentGroup.objects.filter(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=6,
                        group_id=7,
                        is_active=False,
                    ).update(is_active=True)
                try:
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=7,
                        group_id=7,
                    )
                except:
                    UserCompanyComponentGroup.objects.filter(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=7,
                        group_id=7,
                        is_active=False,
                    ).update(is_active=True)
                try:
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=8,
                        group_id=7,
                    )
                except:
                    UserCompanyComponentGroup.objects.filter(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=8,
                        group_id=7,
                        is_active=False,
                    ).update(is_active=True)
                try:
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=9,
                        group_id=7,
                    )
                except:
                    UserCompanyComponentGroup.objects.filter(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=9,
                        group_id=10,
                        is_active=False,
                    ).update(is_active=True)
                # UserCompanyComponentGroup.objects.create(user_id=new_user.user.id, company_id=companyid, component_id=5, group_id=7)
                # UserCompanyComponentGroup.objects.create(user_id=new_user.user.id, company_id=companyid, component_id=6, group_id=7)
                # UserCompanyComponentGroup.objects.create(user_id=new_user.user.id, company_id=companyid, component_id=7, group_id=7)
                # UserCompanyComponentGroup.objects.create(user_id=new_user.user.id, company_id=companyid, component_id=8, group_id=7)
            else:
                # для Клиента
                try:
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=1,
                        group_id=9,
                    )  # для меню
                except:
                    UserCompanyComponentGroup.objects.filter(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=1,
                        group_id=9,
                        is_active=False,
                    ).update(is_active=True)
                try:
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=6,
                        group_id=9,
                    )  # для своих Задач в CRM
                except:
                    UserCompanyComponentGroup.objects.filter(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=6,
                        group_id=9,
                        is_active=False,
                    ).update(is_active=True)
                try:
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=8,
                        group_id=9,
                    )  # для заказов товара
                except:
                    UserCompanyComponentGroup.objects.filter(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=8,
                        group_id=9,
                        is_active=False,
                    ).update(is_active=True)
                try:
                    UserCompanyComponentGroup.objects.create(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=9,
                        group_id=9,
                    )  # для обращений в техподдержку
                except:
                    UserCompanyComponentGroup.objects.filter(
                        user_id=new_user.user.id,
                        company_id=companyid,
                        component_id=9,
                        group_id=9,
                        is_active=False,
                    ).update(is_active=True)
                # UserCompanyComponentGroup.objects.create(user_id=new_user.user.id, company_id=companyid, component_id=1, group_id=9)   # для меню
                # UserCompanyComponentGroup.objects.create(user_id=new_user.user.id, company_id=companyid, component_id=6, group_id=9)   # для своих Задач в CRM
                # UserCompanyComponentGroup.objects.create(user_id=new_user.user.id, company_id=companyid, component_id=8, group_id=9)   # для заказов товара
            return render(
                request,
                "registration/register_done.html",
                {
                    "new_user": new_user.user,
                    "param": "add",
                    "companyid": companyid,
                },
            )
    else:
        comp = Company.objects.get(id=companyid)
        user_form = UserAddForm(instance=comp)
    return render(
        request,
        "registration/register.html",
        {"user_form": user_form, "param": "add", "companyid": companyid},
    )


def invite(request, companyid=1):
    if request.method == "POST":
        user_form = UserInviteForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            pss = user_form.cleaned_data["password"]
            new_user.set_password(pss)
            # Save the User object
            new_user.save()

            UserProfile.objects.create(
                user_id=new_user.id,
                company_id=companyid,
                is_notify=True,
                protocoltype_id=1,
                description="Профиль создан Администратором Организации",
            )
            if new_user.is_staff == True:
                # для Сотрудника
                UserCompanyComponentGroup.objects.create(
                    user_id=new_user.id,
                    company_id=companyid,
                    component_id=1,
                    group_id=7,
                )
                # UserCompanyComponentGroup.objects.create(user_id=new_user.id, company_id=companyid, component_id=4, group_id=7)  #доступ к Организации д.б. только у Админа Организации (group_id=2)
                UserCompanyComponentGroup.objects.create(
                    user_id=new_user.id,
                    company_id=companyid,
                    component_id=5,
                    group_id=7,
                )
                UserCompanyComponentGroup.objects.create(
                    user_id=new_user.id,
                    company_id=companyid,
                    component_id=6,
                    group_id=7,
                )
                UserCompanyComponentGroup.objects.create(
                    user_id=new_user.id,
                    company_id=companyid,
                    component_id=7,
                    group_id=7,
                )
                UserCompanyComponentGroup.objects.create(
                    user_id=new_user.id,
                    company_id=companyid,
                    component_id=8,
                    group_id=7,
                )
            else:
                # для Клиента
                UserCompanyComponentGroup.objects.create(
                    user_id=new_user.id,
                    company_id=companyid,
                    component_id=1,
                    group_id=9,
                )  # для меню
                UserCompanyComponentGroup.objects.create(
                    user_id=new_user.id,
                    company_id=companyid,
                    component_id=6,
                    group_id=9,
                )  # для своих Задач в CRM
                UserCompanyComponentGroup.objects.create(
                    user_id=new_user.id,
                    company_id=companyid,
                    component_id=8,
                    group_id=9,
                )  # для заказов товара

            site_name = get_current_site(request)
            text_plain = (
                "Вы приглашены в Систему 1YES! по адресу: http://"
                + str(site_name)
                + "/accounts/login\r\nЛогин: "
                + new_user.username
                + "r\n\Пароль: "
                + pss
                + "r\n\r\n\Добро пожаловать в нашу команду!"
            )
            text_html = (
                '<p>Вы приглашены в Систему 1YES! по адресу: <a href="http://'
                + str(site_name)
                + '/accounts/login">http://'
                + str(site_name)
                + "/accounts/login</a></p><p>Логин: "
                + new_user.username
                + "</p><p>Пароль: "
                + pss
                + "</p><p>Добро пожаловать в нашу команду!</p>"
            )
            send_mail(
                "1YES! Приглашение в Систему",
                text_plain,
                settings.EMAIL_HOST_USER,
                [new_user.email],
                html_message=text_html,
            )
            return render(
                request,
                "registration/register_done.html",
                {
                    "new_user": new_user,
                    "param": "invite",
                    "companyid": companyid,
                },
            )
    else:
        user_form = UserInviteForm()
    return render(
        request,
        "registration/register.html",
        {"user_form": user_form, "param": "invite", "companyid": companyid},
    )


#
# class UserProfileDetail(DetailView):
#    model = UserProfile
#    template_name = 'userprofile_detail.html'
#
#    def get_queryset(self):
#        return UserProfile.objects.filter(user_id=self.request.user.id) #self.kwargs['userid'])
#


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def UserProfileDetail(request, userid=0, param=""):
    companies_id = request.session["_auth_user_companies_id"]
    OurTZ = pytz.timezone("Europe/Moscow")

    if userid == 0:
        userid = request.user.id
        if param == "all":
            # content_list = Content.objects.filter(author_id=userid, is_forprofile=True).annotate(cnt=Count('id'))
            # content_list = Content.objects.filter(author_id=userid, place_id=3).annotate(cnt=Count('id'))
            content_list = Content.objects.filter(author_id=userid).annotate(
                cnt=Count("id")
            )

            # *** потестируем забор контента с произвольного сайта ***
            # parsing_test()
            # ***
        else:
            content_list = Content.objects.filter(
                author_id=userid,
                is_active=True,
                datebegin__lte=datetime.now(OurTZ),
                dateend__gte=datetime.now(OurTZ),
                place_id=3,
            ).annotate(cnt=Count("id"))
    else:
        content_list = Content.objects.filter(
            author_id=userid,
            is_active=True,
            datebegin__lte=datetime.now(OurTZ),
            dateend__gte=datetime.now(OurTZ),
            place_id=3,
        ).annotate(cnt=Count("id"))

    # user_profile = UserProfile.objects.get(user=userid, is_active=True) #.company_id
    user_profile = (
        UserProfile.objects.filter(user=userid, is_active=True)
        .select_related("company", "user", "protocoltype")
        .first()
    )
    notification_list = Notification.objects.filter(
        recipient_id=userid, is_active=True, is_read=False, type_id=3
    ).select_related("author", "type", "recipient", "objecttype")
    # print(notification_list)
    # table = NotificationTable(notification_list)
    metaobjecttype_list = Meta_ObjectType.objects.filter(is_active=True)

    # button_project_create = ''
    button_userprofile_update = "Изменить"
    prompt_is_notify = "Вкл."
    if user_profile:
        if user_profile.is_notify == False:
            prompt_is_notify = "Выкл."

    return render(
        request,
        "userprofile_detail.html",
        {
            "user_profile": user_profile,
            "button_userprofile_update": button_userprofile_update,
            "content_list": content_list,
            "user_companies": companies_id,
            "prompt_is_notify": prompt_is_notify,
            "notification_list": notification_list.distinct().order_by("-datecreate"),
            "metaobjecttype_list": metaobjecttype_list.distinct().order_by(),
            "status_selectid": "2",
            "metaobjecttype_selectid": "0",
            #'table': table,
        },
    )


class UserProfileUpdate(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "object_form.html"
    # success_url = '../3'

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdate, self).get_context_data(**kwargs)
        context["header"] = "Изменить Профиль"
        return context

    def get_form_kwargs(self):
        kwargs = super(UserProfileUpdate, self).get_form_kwargs()
        # здесь нужно условие для 'action': 'update'
        kwargs.update({"org": self.request.session["_auth_user_companies_id"]})
        return kwargs

    # записываем новое значение текущей компании из профиля в переменную сессии
    def form_valid(self, form):
        # form.instance.user = self.request.user
        form.save()
        current_company = UserProfile.objects.get(
            user=self.request.user.id, is_active=True
        ).company_id
        self.request.session["_auth_user_currentcompany_id"] = current_company
        return super(UserProfileUpdate, self).form_valid(form)


def parsing_test():
    url0 = "https://bobsoccer.ru"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)"
    }

    for count in range(1, 3):
        sleep(3)
        url = url0 + f"/tags/?tag=%D0%A6%D0%A1%D0%9A%D0%90&part={count}"
        r = requests.get(url, headers=headers)
        soup = BS(r.text, "lxml")
        data = soup.find_all("div", class_="blog-list")
        for el in data:
            datetime = el.find("time").get("datetime")
            title = el.find("h2").text.replace("\n", "")
            summary = el.find("p").text.replace("\n", "")
            link = url0 + el.find("a").get("href")
            print("Страница ", count)
            print(datetime)
            print(title)
            print(summary)
            print(link)
            # вытаскиваем текст поста
            r1 = requests.get(link, headers=headers)
            soup1 = BS(r1.text, "lxml")
            data1 = soup1.find_all("div", class_="blog-element")
            for el1 in data1:
                description = el1.find_all("p")[1].text
                print(
                    description.encode("utf-8", errors="ignore").decode(
                        "utf-8", errors="ignore"
                    )
                )
            print("\n")

    return
