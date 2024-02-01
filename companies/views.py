from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime, date, time
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.template import loader, Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.db.models import Q

from .models import (
    Company,
    UserCompanyComponentGroup,
    StaffList,
    Staff,
    Summary,
    Content,
    Dict_ContentType,
    Dict_ContentPlace,
)
from main.models import Component
from django.contrib.auth.models import Group

# from projects.models import Project, Task, TaskComment
from .forms import (
    CompanyForm,
    StaffListForm,
    StaffForm,
    StaffUpdateForm,
    SummaryForm,
    ContentForm,
)

# class CompaniesList(ListView):
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

# def companies_main(request):
#    companies_list = Company.objects.filter(is_active=True)
#    #companies_list = Company.objects.all()
#    return render(request, 'menu_companies.html', {
#                              'node': companies_list, #Company.objects.all(),
#                              'user_companies': request.session['_auth_user_companies_id'],
#                                             }
#                 )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def companies(request, pk=0, razdel="projects"):
    comps = request.session["_auth_user_companies_id"]
    if pk == 0:
        current_company = 0
        tree_company_id = 0
        root_company_id = 0
        tree_company_id = 0
        project_id = 0
        # template_name = "menu_companies.html"
        # print(comps)
    else:
        current_company = (
            Company.objects.filter(id=pk)
            .select_related("author", "currency", "structure_type", "type")
            .first()
        )
        tree_company_id = current_company.tree_id
        root_company_id = current_company.get_root().id
        tree_company_id = current_company.tree_id
        try:
            current_project = current_company.resultcompany.all()[0].id
        except (ValueError, IndexError) as e:
            project_id = 0
        else:
            project_id = current_project

    # здесь нужно условие для button_company_create
    button_company_create = ""
    button_company_create = _("Добавить")
    button_StaffList = _("Штатное расписание")

    component_name = razdel
    request.session["_auth_user_currentcomponent"] = component_name
    template_name = "companies.html"

    is_many_support_member = True

    if razdel == "feedback":
        # is_support_member = request.session['_auth_user_issupportmember']
        # сотрудникам Техподдержки показывать только те компании, где они работают
        # это неправильно, ибо они тоже должны иметь возможность обращаться в другие техподдержки!
        # if is_support_member:
        #    nodes = Company.objects.filter(is_active=True, is_support=True, id__in=comps)
        #    if len(nodes) == 1:
        #        # если пользователь является сотрудником только одной Техподдержки, то он не может выбрать другую службу
        #        is_many_support_member = False
        # else:
        nodes = Company.objects.filter(is_active=True, is_support=True)
    else:
        nodes = Company.objects.filter(is_active=True, id__in=comps)
    # nodes = nodes.order_by("tree_id", "level")

    return render(
        request,
        template_name,
        {
            "nodes": nodes.select_related(
                "author", "currency", "structure_type", "type"
            ),
            "len_list": len(nodes),
            "current_company": current_company,
            "root_company_id": root_company_id,
            "tree_company_id": tree_company_id,
            "project_id": project_id,
            "user_companies": comps,  # request.session['_auth_user_companies_id'],
            "button_company_create": button_company_create,
            "button_StaffList": button_StaffList,
            "object_list": "company_list",
            "component_name": component_name,
            "is_many_support_member": is_many_support_member,
        },
    )


def tree_get_root(request, pk):
    current_company = Company.objects.get(id=pk)
    root_company_id = current_company.get_root().id
    return root_company_id


class CompanyDetail(DetailView):
    model = Company
    template_name = "company_detail.html"


class CompanyCreate(CreateView):
    model = Company
    form_class = CompanyForm
    # template_name = 'project_create.html'
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if self.kwargs["parentid"] != 0:
            form.instance.parent_id = self.kwargs["parentid"]

        if form.is_valid():
            org = form.save()
            UserCompanyComponentGroup.objects.create(
                user_id=form.instance.author_id,
                company_id=org.id,
                component_id=5,
                group_id=1,
            )

        return super(CompanyCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CompanyCreate, self).get_context_data(**kwargs)
        context["header"] = "Новая Организация"
        return context


class CompanyUpdate(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Организацию")
        return context


# def getCompanies(request, user):
#     #uc = UserCompany.objects.get(user=user)
#     return render(request, "menu_companies.html", {'nodes':request.UserCompany.objects.get(user=user)})


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def stafflist(request, companyid=0, pk=0):
    currentuser = request.user.id

    if companyid == 0:
        companyid = request.session["_auth_user_currentcompany_id"]

    comps = request.session["_auth_user_companies_id"]
    current_company = (
        Company.objects.filter(id=companyid)
        .select_related("author", "currency", "structure_type", "type")
        .first()
    )

    if pk == 0:
        current_stafflist = 0
        tree_stafflist_id = 0
        root_stafflist_id = 0
        tree_stafflist_id = 0
        stafflist_id = 0
        # template_name = "stafflist.html"
    else:
        current_stafflist = (
            StaffList.objects.filter(id=pk)
            .select_related("author", "company", "currency", "type")
            .first()
        )
        tree_stafflist_id = current_stafflist.tree_id
        root_stafflist_id = current_stafflist.get_root().id
        tree_stafflist_id = current_stafflist.tree_id
    template_name = "company_detail.html"

    # здесь нужно условие для button_stafflist_create
    # button_stafflist_create = ''
    button_stafflist_create = _("Добавить")
    # button_stafflist = "Штатное расписание"

    button_company_select = _("Сменить организацию")
    comps = request.session["_auth_user_companies_id"]
    if len(comps) > 1:
        button_company_select = _("Сменить организацию")

    component_name = "companies"
    #  unodes = UserCompanyComponentGroup.objects.filter(is_active=True, company_id=companyid).exclude(user_id=currentuser).distinct().order_by('user_id')
    #  unodes = UserCompanyComponentGroup.objects.filter(is_active=True, company_id=companyid).distinct().order_by('user_id')
    #  raw_query = 'SELECT * FROM companies_usercompanycomponentgroup uc LEFT JOIN auth_user u ON u.id=uc.user_id LEFT JOIN companies_company c ON
    # c.id=uc.company_id LEFT JOIN main_component cmp ON cmp.id=uc.component_id LEFT JOIN auth_group g ON g.id=uc.group_id WHERE company_id='+str(companyid)+' AND uc.is_active=1 AND u.is_active=1 GROUP BY  uc.user_id'
    raw_query_1 = "SELECT * FROM companies_usercompanycomponentgroup uc LEFT JOIN auth_user u ON u.id=uc.user_id LEFT JOIN main_component c ON c.id=uc.component_id "
    raw_query_2 = (
        "WHERE uc.company_id="
        + str(
            companyid
            # ) + " AND uc.is_active=1 AND u.is_active=1 AND c.code='" + component_name + "' GROUP BY uc.user_id"
        )
        + " AND uc.is_active=1 AND u.is_active=1 GROUP BY uc.user_id"
    )
    raw_query = raw_query_1 + raw_query_2
    # print(raw_query)
    unodes = UserCompanyComponentGroup.objects.raw(raw_query)

    # print(companyid, unodes)
    nodes = (
        StaffList.objects.filter(is_active=True, company_id=companyid)
        .select_related("author", "company", "currency", "type")
        .order_by()
    )

    button_company_create = ""
    button_company_update = ""
    button_user_invite = ""
    button_user_create = ""
    button_stafflist_create = ""
    # print(unodes)
    # print(current_company.author_id)
    if currentuser == current_company.author_id:
        button_company_create = _("Добавить")
        button_company_update = _("Изменить")
        button_user_invite = _("Пригласить")
        button_user_create = _("Добавить")
        if len(nodes) == 0:
            # в Компании может быть только один руководитель!
            button_stafflist_create = "Добавить"

    return render(
        request,
        template_name,
        {
            "unodes": unodes,
            "nodes": nodes,
            "current_stafflist": current_stafflist,
            "root_stafflist_id": root_stafflist_id,
            "tree_stafflist_id": tree_stafflist_id,
            "current_company": current_company,
            "companyid": companyid,
            "user_companies": comps,
            "button_company_select": button_company_select,
            "button_company_create": button_company_create,
            "button_company_update": button_company_update,
            # 'button_StaffList': button_stafflist,
            "button_user_invite": button_user_invite,
            "button_user_create": button_user_create,
            "button_stafflist_create": button_stafflist_create,
            "object_list": "stafflist_list",
            "component_name": component_name,
        },
    )


# class StaffListDetail(DetailView):
#    model = StaffList
#    template_name = 'stafflist_detail.html'


class StaffListCreate(CreateView):
    model = StaffList
    form_class = StaffListForm
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.company_id = self.kwargs["companyid"]
        if self.kwargs["parentid"] != 0:
            form.instance.parent_id = self.kwargs["parentid"]
        return super(StaffListCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(StaffListCreate, self).get_context_data(**kwargs)
        context["header"] = "Новая Должность"
        return context


class StaffListUpdate(UpdateView):
    model = StaffList
    form_class = StaffListForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(StaffListUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Должность")
        return context


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def staffs(request, stafflistid=0, pk=0):
    currentuser = request.user.id

    # if companyid == 0:
    #   companyid = request.session['_auth_user_currentcompany_id']

    comps = request.session["_auth_user_companies_id"]
    current_stafflist = (
        StaffList.objects.filter(id=stafflistid)
        .select_related("author", "company", "currency", "type")
        .first()
    )
    current_company = (
        Company.objects.filter(id=current_stafflist.company_id)
        .select_related("author", "currency", "structure_type", "type")
        .first()
    )

    if pk == 0:
        current_staff = 0
        staff_id = 0
        # template_name = "stafflist.html"
    else:
        current_staff = Staff.objects.get(id=pk)
    template_name = "stafflist_detail.html"

    # здесь нужно условие для button_stafflist_create
    button_stafflist_create = ""
    button_stafflist_create = _("Добавить")
    # button_stafflist = _("Штатное расписание")

    # button_company_select = _('Сменить организацию')
    comps = request.session["_auth_user_companies_id"]
    # if len(comps) > 1:
    #   button_company_select = _('Сменить организацию')

    component_name = "companies"

    # number_employees = Staff.objects.filter(Q(dateend__gte=datetime.now()) | Q(dateend=None), datebegin__lte=datetime.now(), is_active=True, stafflist_id=stafflistid).annotate(cnt=Count('id'))
    nodes = (
        Staff.objects.filter(
            Q(dateend__gte=datetime.now()) | Q(dateend=None),
            datebegin__lte=datetime.now(),
            is_active=True,
            stafflist_id=stafflistid,
        )
        .select_related("author", "stafflist", "user")
        .order_by()
    )

    button_stafflist_create = ""
    button_stafflist_update = ""
    button_staff_create = ""
    # button_staff_update = ''
    if currentuser == current_company.author_id:
        # print(number_employees.cnt)
        # if number_employees[0].cnt < current_stafflist.numberemployees:
        if len(nodes) < current_stafflist.numberemployees:
            button_staff_create = _("Добавить")
        button_stafflist_create = _("Добавить")
        button_stafflist_update = _("Изменить")
        # button_staff_update = _('Изменить')

    return render(
        request,
        template_name,
        {
            # 'nodes': Staff.objects.filter(is_active=True, stafflist_id=stafflistid).order_by(),
            # надо выводить только действующих Сотрудников (по датам)
            "nodes": nodes,
            "current_stafflist": current_stafflist,
            # 'current_company': current_company,
            # 'companyid': companyid,
            "user_companies": comps,
            # 'button_company_create' : button_company_create,
            # 'button_company_update' : button_company_update,
            # 'button_stafflist_create': button_stafflist_create,
            # 'button_StaffList': button_stafflist,
            # 'object_list': 'stafflist_list',
            "component_name": component_name,
            # 'button_company_select' : button_company_select,
            "button_stafflist_create": button_stafflist_create,
            "button_stafflist_update": button_stafflist_update,
            "button_staff_create": button_staff_create,
        },
    )


class StaffCreate(CreateView):
    model = Staff
    form_class = StaffForm
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        # if self.kwargs['parentid'] != 0:
        #   form.instance.parent_id = self.kwargs['parentid']

        # if form.is_valid():
        #   org = form.save()
        #   UserCompanyComponentGroup.objects.create(user_id=form.instance.author_id,
        #                                            company_id=org.id,
        #                                            component_id=5,
        #                                            group_id=1)

        return super(StaffCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(StaffCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новый Сотрудник")  # + stafflistid
        return context

    def get_form_kwargs(self):
        kwargs = super(StaffCreate, self).get_form_kwargs()
        kwargs.update(
            {
                "user": self.request.user,
                "action": "create",
                "stafflistid": self.kwargs["stafflistid"],
            }
        )
        return kwargs


class StaffUpdate(UpdateView):
    model = Staff
    form_class = StaffUpdateForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(StaffUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Должность")
        return context

    def get_form_kwargs(self):
        kwargs = super(StaffUpdate, self).get_form_kwargs()
        # kwargs.update({'user': self.request.user, 'action': 'update'})
        kwargs.update({"user": self.request.user})
        return kwargs


def vacancies(request):
    template_name = "index.html"
    vacancies_list = StaffList.objects.filter(is_vacancy=True)
    param = "vacancies"
    return render(
        request,
        template_name,
        {
            "vacancies_list": vacancies_list,
            "param": param,
        },
    )


def vacancy_detail(request, pk):
    template_name = "vacancy_detail.html"
    current_stafflist = StaffList.objects.get(id=pk)
    button_send_resume = _("Откликнуться на вакансию")
    return render(
        request,
        template_name,
        {
            "current_stafflist": current_stafflist,
            "button_send_resume": button_send_resume,
            "stafflistid": current_stafflist.id,
        },
    )


class SummaryCreate(CreateView):
    model = Summary
    form_class = SummaryForm
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.stafflist_id = self.kwargs["stafflistid"]
        return super(SummaryCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SummaryCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новое резюме")
        return context

    # def get_form_kwargs(self):
    #   kwargs = super(SummaryCreate, self).get_form_kwargs()
    #   kwargs.update({'action': 'create', 'stafflistid': self.kwargs['stafflistid']})
    #   return kwargs


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def summaries(request, pk=0):
    template_name = "stafflist_detail.html"
    if pk == 0:
        summaries_list = Summary.objects.filter(
            is_active=True, stafflist__is_active=True, stafflist__is_vacancy=True
        )
    else:
        summaries_list = Summary.objects.filter(
            stafflist_id=pk,
            is_active=True,
            stafflist__is_active=True,
            stafflist__is_vacancy=True,
        )
    summaries_list = summaries_list.select_related("stafflist").order_by("-datecreate")
    param = "summaries"
    comps = request.session["_auth_user_companies_id"]
    current_stafflist = (
        StaffList.objects.filter(id=pk)
        .select_related("author", "company", "currency", "type")
        .first()
    )
    button_stafflist_create = _("Добавить")
    button_stafflist_update = _("Изменить")
    return render(
        request,
        template_name,
        {
            "summaries_list": summaries_list,
            "param": param,
            "user_companies": comps,
            "current_stafflist": current_stafflist,
            "button_stafflist_create": button_stafflist_create,
            "button_stafflist_update": button_stafflist_update,
        },
    )


def summary_detail(request, pk):
    template_name = "summary_detail.html"
    current_summary = Summary.objects.filter(id=pk).select_related("stafflist").first()
    if not current_summary.candidatemiddlename:
        current_summary.candidatemiddlename = ""
    button_delete_resume = _("Удалить резюме")
    return render(
        request,
        template_name,
        {
            "current_summary": current_summary,
            "button_delete_resume": button_delete_resume,
        },
    )


def summary_delete(request, pk):
    template_name = "summary_detail.html"
    current_summary = Summary.objects.filter(id=pk).select_related("stafflist").first()
    if current_summary.is_active == True:
        current_summary.is_active = False
        button_delete_resume = _("Восстановить резюме")
    else:
        current_summary.is_active = True
        button_delete_resume = _("Удалить резюме")
    current_summary.save()

    return render(
        request,
        template_name,
        {
            "current_summary": current_summary,
            "button_delete_resume": button_delete_resume,
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def contents(request, place=0):
    template_name = "main.html"
    if place == 1:
        template_name = "userprofile_detail.html"

    # if user.is_authenticated:
    companies_id = request.session["_auth_user_companies_id"]
    content_list = ""
    if request.user.is_authenticated:
        # content_list = Content.objects.filter(is_active=True, datebegin__lte=datetime.now(), dateend__gte=datetime.now(), company__is_active=True, company_id__in=companies_id)
        # result=list(set(companies_id) & set(Word)) # - пример пересечения множеств
        if place == 0:
            content_list = Content.objects.filter(
                is_active=True,
                datebegin__lte=datetime.now(),
                dateend__gte=datetime.now(),
                company__is_active=True,
                company__in=companies_id,
                place_id=2,
            ).annotate(cnt=Count("id"))
        else:
            content_list = Content.objects.filter(
                is_active=True,
                datebegin__lte=datetime.now(),
                dateend__gte=datetime.now(),
                company__is_active=True,
                company__in=companies_id,
                place_id=3,
            ).annotate(cnt=Count("id"))
            # это надо как-то исправить, чтоб записи не дублировались, когда контент для нескольких компаний, и они же есть в списке у пользователя!
    content_list = content_list.select_related("author", "type", "place")
    # здесь нужно условие для button_company_create
    # юзер имеет право на добавление контента
    # это реализовано в шаблоне через штатный perms.companies.add_content
    button_content_create = ""
    #  is_add2 = 'SELECT p.id FROM auth_user_groups ug INNER JOIN auth_user u ON u.id=ug.user_id INNER JOIN auth_group_permissions gp ON gp.group_id=ug.group_id INNER JOIN auth_permission p ON p.id=gp.permission_id WHERE u.is_superuser OR (ug.user_id=2 AND p.codename="add_content")'
    #  is_add1 = 'SELECT p.id FROM auth_user_user_permissions uup INNER JOIN auth_permission p ON p.id=uup.permission_id WHERE uup.user_id=3 AND p.codename="add_content"'
    #  is_add.query = auth_user_user_permissions.objects.filter(user_id=3, auth_permission__codename='add_content').values('auth_permission__id')
    #  u = User.objects.add_content(username='larimarit')
    #  is_add = u.has_perm('add_content')
    #  if is_add:
    #    button_content_create = 'Добавить'
    #  else:
    #    if is_add2:
    #       button_content_create = 'Добавить'
    #  print(template_name)
    return render(
        request,
        template_name,
        {
            "content_list": content_list,
            "user_companies": companies_id,  # request.session['_auth_user_companies_id'],
            "button_content_create": button_content_create,
        },
    )


def publiccontents(request):
    template_name = "index.html"
    # content_list = Content.objects.filter(is_active=True, datebegin__lte=datetime.now(), dateend__gte=datetime.now(), company__is_active=True, is_public=True, is_forprofile=False, is_private=False).annotate(cnt=Count('id'))
    content_list = (
        Content.objects.filter(
            is_active=True,
            datebegin__lte=datetime.now(),
            dateend__gte=datetime.now(),
            company__is_active=True,
            place__is_active=True,
            place_id=1,
        )
        .select_related("author", "type", "place")
        .annotate(cnt=Count("id"))
    )
    param = "publiccontent"
    return render(
        request,
        template_name,
        {
            "content_list": content_list,
            "param": param,
        },
    )


class ContentList(ListView):
    model = Content
    # template_name = 'content.html'
    template_name = "main.html"

    # ordering = ['company_up', 'id']

    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            # current_membership = get_user_membership(self.request)
            # context['current_membership'] = str(current_membership.membership)
            # добавляем к контексту сессионный массив с id компаний, доступными этому авторизованному юзеру
            # button_company_select = 'Сменить организацию'
            context["user_companies"] = self.request.session["_auth_user_companies_id"]
            # context['button_company_select'] = button_company_select
            return context


class ContentDetail(DetailView):
    model = Content
    template_name = "content_detail.html"

    def get_object(self):
        object = super(ContentDetail, self).get_object()
        if not self.request.user.is_authenticated and object.place_id != 1:
            raise Http404
        return object

    def get_context_data(self, *args, **kwargs):
        context = super(ContentDetail, self).get_context_data(**kwargs)
        # print(self.object.name)
        if self.request.user.is_authenticated:
            context["button_content_create"] = _("Добавить")  # button_company_create
            context["button_content_update"] = _("Изменить")
            context["user_companies"] = self.request.session["_auth_user_companies_id"]
            context["whoisauthor"] = _("Автор: ") + self.object.author.username
            if not self.object.is_active:
                context["extdescription"] = _(" (Контент перемещен в архив)")
            return context
        elif self.object.place_id == 1:
            # print(context)
            return context
        # context['extdescription'] = ' Контент недоступен!'

        # return context


class ContentCreate(CreateView):
    model = Content
    form_class = ContentForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(ContentCreate, self).get_context_data(**kwargs)
        context["header"] = _("Новый Контент")
        return context

    def get_form_kwargs(self):
        kwargs = super(ContentCreate, self).get_form_kwargs()
        # здесь нужно условие для 'action': 'create'
        kwargs.update({"org": self.request.session["_auth_user_companies_id"]})
        return kwargs

    def form_valid(self, form):
        # form.instance.company_id = self.kwargs['companyid']
        form.instance.author_id = self.request.user.id
        return super(ContentCreate, self).form_valid(form)


class ContentUpdate(UpdateView):
    model = Content
    form_class = ContentForm
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super(ContentUpdate, self).get_context_data(**kwargs)
        context["header"] = _("Изменить Контент")
        return context

    def get_form_kwargs(self):
        kwargs = super(ContentUpdate, self).get_form_kwargs()
        # здесь нужно условие для 'action': 'update'
        kwargs.update({"org": self.request.session["_auth_user_companies_id"]})
        return kwargs


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def userroles(request, companyid=1, pk=1):
    companyuser = User.objects.filter(id=pk).first()
    companyname = Company.objects.filter(id=companyid).first()
    roles = (
        UserCompanyComponentGroup.objects.filter(
            user_id=pk, company_id=companyid, is_active=True
        )
        .select_related("company", "component", "group", "user")
        .order_by("component_id", "group_id")
    )
    print(pk, roles)
    componentlist = Component.objects.filter(is_active=True)
    grouplist = Group.objects.filter().exclude(name="Суперадминистраторы")
    button_companyuser_update = _("Изменить")
    button_companyuserrole_create = _("Добавить")
    return render(
        request,
        "company_user_detail.html",
        {
            "nodes": roles,
            "companyuser": companyuser,
            "companyid": companyid,
            "companyname": companyname,
            "componentlist": componentlist,
            "grouplist": grouplist,
            "button_companyuser_update": button_companyuser_update,
            "button_companyuserrole_create": button_companyuserrole_create,
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def userrole_delete(request):
    roleid = request.GET["roleid"]
    print(roleid)
    if roleid:
        role = (
            UserCompanyComponentGroup.objects.filter(id=roleid)
            .select_related("user")
            .first()
        )
        role.is_active = 0
        role.save(update_fields=["is_active"])
    return roles_list(
        request,
        role.user_id,
        role.company_id,
        role.component_id,
        role.group_id,
        role.user,
        "",
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def userrole_create(request):
    companyid = request.GET["companyid"]
    userid = request.GET["userid"]
    groupid = request.GET["groupid"]
    componentid = request.GET["componentid"]
    companyuser = User.objects.get(id=userid)
    message = ""
    # try:
    #     role = UserCompanyComponentGroup.objects.create(
    #         user_id=userid,
    #         company_id=companyid,
    #         component_id=componentid,
    #         group_id=groupid)
    #     role.save()
    # except:
    #     message = _('"Эта" роль уже назначена!')
    obj, role = UserCompanyComponentGroup.objects.update_or_create(
        user_id=userid,
        company_id=companyid,
        component_id=componentid,
        group_id=groupid,
        defaults={"is_active": True},
    )
    return roles_list(
        request, userid, companyid, componentid, groupid, companyuser, message
    )


def roles_list(
    request, userid, companyid, componentid, groupid, companyuser, message=""
):
    roles = (
        UserCompanyComponentGroup.objects.filter(
            user_id=userid, company_id=companyid, is_active=True
        )
        .select_related("company", "component", "group", "user")
        .order_by("component_id", "group_id")
    )
    componentlist = Component.objects.filter(is_active=True)
    grouplist = Group.objects.all()
    button_companyuserrole_create = _("Добавить")
    return render(
        request,
        "company_user_roles_list.html",
        {
            "nodes": roles,
            "componentlist": componentlist,
            "grouplist": grouplist,
            "companyuser": companyuser,
            "companyid": companyid,
            "component_selectid": componentid,
            "group_selectid": groupid,
            "message": message,
            "button_companyuserrole_create": button_companyuserrole_create,
        },
    )


def get_current_company(companyid):
    return Company.objects.filter(id=companyid).first()
