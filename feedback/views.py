from django.conf import settings
from django.shortcuts import render
import json, requests

import random, string

from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date, time
from django.db.models import Q, Count, Min, Max, Sum, Avg

from datetime import datetime, date, time


from .serializers import Dict_SystemSerializer, CompanySerializer, FeedbackTicketSerializer, FeedbackTicketCommentSerializer
from companies.models import Company, UserCompanyComponentGroup
from .models import Dict_System, Dict_FeedbackTicketStatus, Dict_FeedbackTicketType, Dict_FeedbackTaskStatus
from .models import FeedbackTicket, FeedbackTicketComment, FeedbackTask, FeedbackTaskComment, FeedbackFile
from .forms import Dict_SystemForm, FeedbackTicketForm, FeedbackTaskForm, FeedbackTicketCommentForm, FeedbackTaskCommentForm

from main.utils import AddFilesMixin

from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, permissions
from .serializers import Dict_SystemSerializer, FeedbackTicketSerializer, FeedbackTicketCommentSerializer
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, requires_csrf_token, csrf_exempt


def get_client_ip(request):
    """  Getting client Ip"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def generate_alphanum_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    print("Alphanum Random string of length", length, "is:", rand_string)

# *** API техподдержки ***

#decorators = [csrf_exempt, requires_csrf_token]
decorators = [csrf_exempt]

@method_decorator(decorators, name='create')
class Dict_SystemViewSet(viewsets.ModelViewSet):
    queryset = Dict_System.objects.all() #.order_by('name')
    serializer_class = Dict_SystemSerializer
    #permission_classes = [permissions.IsAuthenticated]

    #def get_serializer_context(self):
    #    """
    #    Extra context provided to the serializer class.
    #    """
    #    return {
    #        'request': self.request,
    #        'format': self.format_kwarg,
    #        'view': self
    #    }

    #@csrf_exempt
    def create(self, request):
        sys_data = request.data
        ip = sys_data["ip"]
        # Определение ip пришедшего запроса
        #ip = 'кроказябра!'
        new_sys = Dict_System.objects.create(code=sys_data["code"], name=sys_data["name"], domain=sys_data["domain"], url=sys_data["url"], ip=ip, email=sys_data["email"], phone=sys_data["phone"])
        #new_sys = Dict_System.objects.create(name=sys_data["name"], domain=sys_data["domain"], url=sys_data["url"],
        #                                     email=sys_data["email"], phone=sys_data["phone"])
        new_sys.save()
        serializer = Dict_SystemSerializer(new_sys, context={'request': request})
        return Response(serializer.data)

    #def update(self, request, pk=None):
    #    return Response(serializer.data)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all() #.order_by('name')
    serializer_class = CompanySerializer

class FeedbackTicketViewSet(viewsets.ModelViewSet):
    queryset = FeedbackTicket.objects.filter(is_active=True).order_by('-datecreate')
    serializer_class = FeedbackTicketSerializer
    filter_fields = ('name', 'description',)
    """
    #def get(self, request):
    def list(self, request):
        tickets = FeedbackTicket.objects.all()
        serializer = FeedbackTicketSerializer(tickets, many=True)
        return Response({"tickets": serializer.data})
    #def post(self, request):
    def create(self, request):
        ticket = request.data.get("ticket")
        # Create an ticket from the above data
        serializer = FeedbackTicketSerializer(data=ticket)
        if serializer.is_valid(raise_exception=True):
            ticket_saved = serializer.save()
        return Response({"success": "Ticket '{}' created successfully".format(ticket_saved.title)})
    #def put(self, request, pk):
    def retrieve(self, request, pk):
        saved_ticket = get_object_or_404(FeedbackTicket.objects.all(), pk=pk)
        data = request.data.get('ticket')
        serializer = FeedbackTicketSerializer(instance=saved_ticket, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            ticket_saved = serializer.save()
        return Response({
            "success": "Ticket '{}' updated successfully".format(ticket_saved.title)
        })
    """
class FeedbackTicketCommentViewSet(viewsets.ModelViewSet):
    queryset = FeedbackTicketComment.objects.filter(is_active=True).order_by('-datecreate')
    serializer_class = FeedbackTicketCommentSerializer
    #filter_fields = ('username', 'is_player', 'first_name', 'last_name', 'team', 'email',)

#def FeedbackTicketCreateAPI(request):
#    return

# ******

class Dict_SystemCreate(CreateView):
    model = Dict_System
    form_class = Dict_SystemForm
    #template_name = 'feedbackticket_create.html'
    template_name = 'object_form.html'

    #def get_success_url(self):
    #    print(self.object) # Prints the name of the submitted user
    #    print(self.object.id) # Prints None
    #    return reverse("webApp:feedbackticket:stepTwo", args=(self.object.id,))

    def form_valid(self, form):
    #    form.instance.system_id = self.kwargs['systemid']
    #    form.instance.company_id = self.kwargs['companyid']
    #    form.instance.author_id = self.request.user.id
    #    form.instance.companyfrom_id = self.request.session['_auth_user_currentcompany_id']
    #    form.instance.status_id = 1 # Новому Тикету присваиваем статус "Новый"
    #    #form.instance.system_id = 1  # Новый Тикет временно приписываем к локальной Системе
        self.object = form.save() # Созадём новую Систему
        ##print(dsys_cnt)
        # http_host = request.META['HTTP_HOST']
        ##print(http_host)
        ##dsys = Dict_System.objects.create(code='===', name='1YES!', domain=http_host, url=http_host, is_active=True)
        ##dsys.save()
        # *** Добавление системы в удалённую БД ***
        ip = get_client_ip(self.request)
        # генерация уникального кода для регистрируемой Системы
        code = generate_alphanum_random_string(4) + '-' + generate_alphanum_random_string(4) + '-' + generate_alphanum_random_string(4) + '-' + generate_alphanum_random_string(4)
        print('ip=', ip, '   code=', code)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        #system_data = {'name': self.object.name, 'domain': self.object.domain, 'url': self.object.url, 'ip': self.object.ip, 'email': self.object.email, 'phone': self.object.phone}
        system_data = {'code': code, 'name': self.object.name, 'domain': self.object.domain, 'url': self.object.url, 'ip': ip,
                       'email': self.object.email, 'phone': self.object.phone}
        url = 'http://1yes.larimaritgroup.ru/feedback/api/system/'
        #url = 'http://localhost:8000/feedback/api/system/'
        r = requests.post(url, headers=headers, data=json.dumps(system_data))
        #r = requests.post(url, headers=headers, csrfmiddlewaretoken=csrftoken, data=json.dumps(system_data))
        print(r.status_code)
        #print(self.object.name)
        # ***
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Регистрация новой Системы'
        return context

    #def get_form_kwargs(self):
    #    kwargs = super().get_form_kwargs()
    #    is_support_member = self.request.session['_auth_user_issupportmember']
    #    # здесь нужно условие для 'action': 'create'
    #    kwargs.update({'action': 'create', 'name': self.kwargs['systemid'], 'companyid': self.kwargs['companyid'], 'is_support_member': is_support_member})
    #    return kwargs


def definerights(request, companyid):
    currentuser = request.user.id
    currentusercompanyid = request.session['_auth_user_currentcompany_id']
    is_support_member = False
    is_support_admin_org = False
    is_superadmin = False
    is_admin_org = False
    is_admin = False

    current_company = Company.objects.filter(id=companyid).first()

    if current_company.is_support == True:
        # Является ли юзер сотрудником этой Службы поддержки?
        if companyid in request.session['_auth_user_companies_id']:
            is_support_member = True
        # Является ли юзер Администратором этой Службы поддержки?
        is_support_admin_org = UserCompanyComponentGroup.objects.filter(user_id=currentuser, company_id=companyid,
                                                                group_id=2)
        if is_support_admin_org:
            is_support_admin_org = True

    # Является ли юзер Администратором своей организации?
    is_admin_org = UserCompanyComponentGroup.objects.filter(user_id=currentuser, company_id=currentusercompanyid, group_id=2)
    if is_admin_org:
        is_admin_org = True
        is_admin = True
    # Является ли юзер Суперадмином?
    if 1 in request.session['_auth_user_group_id']:
        #print(usergroupid)
        is_superadmin = True
        is_admin = True
    return(is_support_member, is_support_admin_org, is_admin_org, is_admin, is_superadmin)

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def feedbacktickets(request, companyid=0):

    currentuser = request.user.id
    currentusercompanyid = request.session['_auth_user_currentcompany_id']
    #print(companyid)
    if companyid == 0:
        #companyid = currentusercompanyid
        # Проверяем наличие хоть одной Службы поддержки в Системе
        support_list = Company.objects.filter(is_active=True, is_support=True)
        support_count = len(support_list)
        #print(support_count)
        if support_count == 0:
            # В системе нет ни одной Службы техподдержки!
            return render(request, "companies.html", {'len_list':0})
        elif support_count == 1:
            # В системе только одна Служба техподдержки
            companyid = support_list[0].id
            #print('1/',support_list[0].name)
        else:
            # В системе несколько Служб техподдержки.
            try:
                # Пробуем выбрать по последнему отправленному тикету
                mylastticket = FeedbackTicket.objects.filter(is_active=True, author_id=currentuser).order_by('-id')[0]
                companyid = mylastticket.company_id
                #print('2/+++', mylastticket.company.name)
            except:
                # если тикет не найден, то выбираем первую Службу техподдержки
                companyid = support_list[0].id
                #print('2/---',support_list[0].name)

    #mycompanies = '_auth_user_companies_id'
    #mysupportcompany = Company.objects.filter(is_active=True, id__in=mycompanies)[0]
    current_company = Company.objects.filter(id=companyid).first()

    request.session['_auth_user_currentcomponent'] = 'feedback'

    # Видимость пункта "- Все" в фильтрах
    (is_support_member, is_support_admin_org, is_admin_org, is_admin, is_superadmin) = definerights(request,companyid)

    request.session['_auth_user_issupportmember'] = is_support_member
    #if is_support_member:
    #    request.session['_auth_user_supportcompany_id'] = companyid
    #else:
    #    request.session['_auth_user_supportcompany_id'] = currentusercompanyid
    request.session['_auth_user_supportcompany_id'] = companyid

    # *** фильтруем по статусу ***
    tktstatus_selectid = 0
    #mytktstatus = 0 # для фильтра "Мои проекты"
    try:
       tktstatus = request.POST['select_feedbackticketstatus']
    except:
        if is_support_member:
            feedbackticket_list = FeedbackTicket.objects.filter(is_active=True,
                                                                company=companyid, dateclose__isnull=True)
        else:
            feedbackticket_list = FeedbackTicket.objects.filter(Q(author=request.user.id), is_active=True,
                                                                company=companyid, dateclose__isnull=True)
    else:
       if tktstatus == "0":
           # если в выпадающем списке выбрано "Все активные"
           feedbackticket_list = FeedbackTicket.objects.filter(Q(author=request.user.id), is_active=True, company=companyid, dateclose__isnull=True)
       else:
          if tktstatus == "-1":
             # если в выпадающем списке выбрано "Все"
             if is_superadmin:
                # Суперадмин видит все тикеты всех организаций этой Службы поддержки
                feedbackticket_list = FeedbackTicket.objects.filter(Q(author=request.user.id), is_active=True, company=companyid)
             elif is_admin_org:
                 # Админ Организации видит все тикеты своей организации этой Службы поддержки
                feedbackticket_list = FeedbackTicket.objects.filter(Q(author=request.user.id), is_active=True,
                                                                     company=companyid, companyfrom=currentusercompanyid)
          elif tktstatus == "-2":
             # если в выпадающем списке выбрано "Просроченные"
             feedbackticket_list = FeedbackTicket.objects.filter(Q(author=request.user.id), is_active=True, company=companyid, dateclose__isnull=True, dateend__lt=datetime.datetime.now())
          else:
             feedbackticket_list = FeedbackTicket.objects.filter(Q(author=request.user.id), is_active=True, company=companyid, status=tktstatus) #, dateclose__isnull=True)
       tktstatus_selectid = tktstatus
    #tktstatus_myselectid = mytktstatus
    # *******************************
    #feedbackticket_list = feedbackticket_list.order_by('dateclose')

    button_feedbackticketdev_create = ''
    len_task_list = 0
    if is_support_member == True:
        feedbackticket_task_list = FeedbackTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id), is_active=True, ticket__company=companyid,
                                                        dateclose__isnull=True)
        len_task_list = len(feedbackticket_task_list)
        #print(len_task_list)
        button_feedbackticketdev_create = 'Обращение к разработчику'

    len_list = len(feedbackticket_list)

    #obj_files_rights = 0
    #if pk == 0:
    #   current_feedbackticket = 0
    #else:
    #   current_feedbackticket = FeedbackTicket.objects.get(id=pk)
    #   if currentuser == current_feedbackticket.author_id or currentuser == current_feedbackticket.assigner_id:
    #       obj_files_rights = 1

    comps = request.session['_auth_user_companies_id']

    # Заполняем списки справочников для фильтров
    # Статусы и Типы берём из списка тикетов всей компании (это неправильно, ибо тогда при выборе одного элемента нельзя будет вернуться к полному списку)
    #all_list = FeedbackTicket.objects.filter(is_active=True, company=companyid)
    #status_list = all_list.values('status_id')
    #types_list = all_list.values('type_id')
    #ticketstatus = Dict_FeedbackTicketStatus.objects.filter(id__in=status_list)
    #tickettype = Dict_FeedbackTicketType.objects.filter(id__in=types_list)
    ticketstatus = Dict_FeedbackTicketStatus.objects.filter(is_active=True)
    tickettype = Dict_FeedbackTicketType.objects.filter(is_active=True)

    #button_company_select = ''
    button_company_select = 'Сменить службу техподдержки'
    button_feedbackticket_create = 'Добавить'
    # Проверяем кол-во компаний - служб техподдержки
    #comps_support = Company.objects.filter(is_active=True, is_support=True)
    is_many_support_member = True
    is_support_member = request.session['_auth_user_issupportmember']
    if is_support_member:
        # сотрудникам Техподдержки показывать только те компании, где они работают
        comps_support = Company.objects.filter(is_active=True, is_support=True, id__in=comps)
        if len(comps_support) == 1:
            # если пользователь является сотрудником только одной Техподдержки, то он не может выбрать другую службу
            is_many_support_member = False
            button_company_select = ''

        # Список всех задач этого сотрудника этой техподдержки
        #task_list = FeedbackTask.objects.filter(
        #                    Q(author=request.user.id) | Q(assigner=request.user.id), ticket__company_id=currentusercompanyid,
        #                    is_active=True, dateclose__isnull=True)
        task_list = FeedbackTask.objects.filter(
            Q(author=request.user.id) | Q(assigner=request.user.id), ticket__company_id=current_company.id,
            is_active=True, dateclose__isnull=True)
    else:
        comps_support = Company.objects.filter(is_active=True, is_support=True)
        if len(comps_support) < 2:
            button_company_select = ''
        task_list = ''

    # Добавляем Систему в справочник
    is_system_reged = True
    dsys_cnt = Dict_System.objects.filter(is_active=True).count()
    if dsys_cnt == 0:
        is_system_reged = False

    return render(request, "company_detail.html", {
                                                  'nodes_tickets': feedbackticket_list.distinct(), #.order_by(), # для удаления задвоений и восстановления иерархии
                                                  'nodes': task_list, #.distinct(), #.order_by(),
                                                  'component_name': 'feedback',
                                                  #'current_feedbackticket': current_feedbackticket,
                                                  'current_company': current_company,
                                                  'current_ticketid': 0,
                                                  'companyid': companyid,
                                                  'user_companies': comps,
                                                  #'obj_files_rights': obj_files_rights,
                                                  'button_company_select': button_company_select,
                                                  'is_system_reged': is_system_reged,
                                                  'button_feedbackticket_create': button_feedbackticket_create,
                                                  'button_feedbackticketdev_create': button_feedbackticketdev_create,
                                                  'feedbackticketstatus': ticketstatus,
                                                  'feedbackticketstatus_selectid': '0',
                                                  'feedbacktickettype': tickettype,
                                                  'feedbacktickettype_selectid': '-1',
                                                  'feedbackticket_myselectid': '1',
                                                  #'tktstatus_myselectid': tktstatus_myselectid,
                                                  'object_list': 'feedbacktask_list',
                                                  #'select_feedbackticketstatus': select_feedbackticketstatus,
                                                  'taskstatus': Dict_FeedbackTaskStatus.objects.filter(is_active=True),
                                                  'len_list': len_list,
                                                  'len_task_list': len_task_list,
                                                  'is_support_member': is_support_member,
                                                  'is_admin': is_admin,
                                                  'is_many_support_member': is_many_support_member,
                                                  #'fullpath': os.path.join(settings.MEDIA_ROOT, '///'),
                                                })


class FeedbackTicketDetail(DetailView):
    model = FeedbackTicket
    template_name = 'feedbackticket_detail.html'


class FeedbackTicketCreate(AddFilesMixin, CreateView):
    model = FeedbackTicket
    form_class = FeedbackTicketForm
    #template_name = 'feedbackticket_create.html'
    template_name = 'object_form.html'

    #def get_success_url(self):
    #    print(self.object) # Prints the name of the submitted user
    #    print(self.object.id) # Prints None
    #    return reverse("webApp:feedbackticket:stepTwo", args=(self.object.id,))

    def form_valid(self, form):
        form.instance.system_id = self.kwargs['systemid']
        form.instance.company_id = self.kwargs['companyid']
        form.instance.author_id = self.request.user.id
        form.instance.companyfrom_id = self.request.session['_auth_user_currentcompany_id']
        form.instance.status_id = 1 # Новому Тикету присваиваем статус "Новый"
        #form.instance.system_id = 1  # Новый Тикет временно приписываем к локальной Системе
        self.object = form.save() # Созадём новый тикет
        af = self.add_files(form, 'feedback', 'ticket') # добавляем файлы из формы (метод из AddFilesMixin)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Новый Тикет'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        is_support_member = self.request.session['_auth_user_issupportmember']
        # здесь нужно условие для 'action': 'create'
        kwargs.update({'user': self.request.user, 'action': 'create', 'systemid': self.kwargs['systemid'], 'companyid': self.kwargs['companyid'], 'is_support_member': is_support_member})
        return kwargs


class FeedbackTicketUpdate(AddFilesMixin, UpdateView):
    model = FeedbackTicket
    form_class = FeedbackTicketForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
        # context = super(ProjectUpdate, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context['header'] = 'Изменить Тикет'
        # kwargs = super(ProjectUpdate, self).get_form_kwargs()
        kwargs = super().get_form_kwargs()
        context['files'] = FeedbackFile.objects.filter(ticket_id=self.kwargs['pk'], is_active=True).order_by('uname')
        # print(context)
        # print(kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        is_support_member = self.request.session['_auth_user_issupportmember']
        # здесь нужно условие для 'action': 'update'
        kwargs.update({'user': self.request.user, 'action': 'update', 'is_support_member': is_support_member})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)  # без commit=False происходит вызов save() Модели
        af = self.add_files(form, 'feedback', 'ticket')  # добавляем файлы из формы (метод из AddFilesMixin)
        comment = form.cleaned_data["comment"]
        self.object = form.save()
        if comment != '':
            # создаём Комментарий к Тикету
            company_id = self.request.session['_auth_user_supportcompany_id']
            cmnt = FeedbackTicketComment.objects.create(ticket_id=self.object.id, company_id=company_id, author_id=form.instance.author_id,
                                                        description=comment)
        return super().form_valid(form)


# *** FeedbackTask ***
@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def feedbacktasks(request, ticketid=0, pk=0):
    # *** фильтруем по статусу ***
    currentuser = request.user.id
    currentusercompanyid = request.session['_auth_user_currentcompany_id']
    #print(currentusercompanyid)
    tskstatus_selectid = 0
    try:
        tskstatus = request.POST['select_taskstatus']
    except:
        task_list = FeedbackTask.objects.filter(
            Q(author=request.user.id) | Q(assigner=request.user.id),
            is_active=True, ticket=ticketid, dateclose__isnull=True)
        #print(task_list)
    else:
        if tskstatus == "0":
            # если в выпадающем списке выбрано "Все активные"
            task_list = FeedbackTask.objects.filter(
                Q(author=request.user.id) | Q(assigner=request.user.id),
                is_active=True, ticket=ticketid, dateclose__isnull=True)
        else:
            if tskstatus == "-1":
                # если в выпадающем списке выбрано "Все"
                task_list = FeedbackTask.objects.filter(
                    Q(author=request.user.id) | Q(assigner=request.user.id),
                    is_active=True, ticket=ticketid)
            elif tskstatus == "-2":
                # если в выпадающем списке выбрано "Просроченные"
                task_list = FeedbackTask.objects.filter(
                    Q(author=request.user.id) | Q(assigner=request.user.id),
                    is_active=True, ticket=ticketid, dateclose__isnull=True, dateend__lt=datetime.now())
            else:
                task_list = FeedbackTask.objects.filter(
                    Q(author=request.user.id) | Q(assigner=request.user.id),
                    is_active=True, ticket=ticketid, status=tskstatus)  # , dateclose__isnull=True)
        tskstatus_selectid = tskstatus
    # *******************************

    len_list = len(task_list)

    currentticket = FeedbackTicket.objects.filter(id=ticketid).first()

    ticketcomment_list = FeedbackTicketComment.objects.filter(ticket_id=ticketid, is_active=True)

    #taskcomment_costsum = FeedbackTaskComment.objects.filter(task__ticket_id=currentticket.id).aggregate(Sum('cost'))
    #taskcomment_timesum = FeedbackTaskComment.objects.filter(task__ticket_id=currentticket.id).aggregate(Sum('time'))
    ticketcomment_costsum = currentticket.costcommentsum
    task_costsum = currentticket.costtasksum
    taskcomment_costsum = currentticket.costtaskcommentsum
    taskcomment_timesum = currentticket.timesum
    try:
        sec = taskcomment_timesum["time__sum"] * 3600
    except:
        sec = 0
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    seconds = sec

    # права на удаление файлов
    obj_files_rights = 0

    if pk == 0:
        current_task = 0
        tree_task_id = 0
        root_task_id = 0
        tree_task_id = 0
        if currentuser == currentticket.author_id:
            obj_files_rights = 1
    else:
        current_task = FeedbackTask.objects.filter(id=pk).first()
        tree_task_id = current_task.tree_id
        root_task_id = current_task.get_root().id
        tree_task_id = current_task.tree_id
        if currentuser == current_task.author_id or currentuser == current_task.assigner_id:
            obj_files_rights = 1

    (is_support_member, is_support_admin_org, is_admin_org, is_admin, is_superadmin) = definerights(request,currentticket.company_id)

    button_feedbackticket_update = ''
    button_ticketcomment_create = ''

    if currentuser == currentticket.author_id or is_support_member: # or is_member:
        button_ticketcomment_create = 'Создать'
        #if currentuser == currentticket.author_id:
        button_feedbackticket_update = 'Изменить'
    button_feedbacktask_create = ''
    if currentticket.company_id in request.session['_auth_user_companies_id'] or is_support_member:
        button_feedbacktask_create = 'Создать'

    return render(request, "feedbackticket_detail.html", {
        'nodes': task_list.distinct().order_by(),  # .order_by('tree_id', 'level', '-dateend'),
        'ticketcommentnodes': ticketcomment_list.distinct().order_by(),
        'len_list': len_list,
        'current_task': current_task,
        'root_task_id': root_task_id,
        'tree_task_id': tree_task_id,
        'is_support_member': is_support_member,
        'current_feedbackticket': currentticket,
        'current_company': currentticket.company,
        'ticketid': ticketid,
        'current_ticketid': ticketid,
        'user_companies': request.session['_auth_user_companies_id'],
        'obj_files_rights': obj_files_rights,
        'files': FeedbackFile.objects.filter(ticket=currentticket, is_active=True).order_by('uname'),
        'objtype': 'fbtsk',
        'media_path': settings.MEDIA_URL,
        #'button_client_create': button_client_create,
        'button_feedbackticket_update': button_feedbackticket_update,
        #'button_client_history': button_client_history,
        'button_feedbacktask_create': button_feedbacktask_create,
        'button_ticketcomment_create': button_ticketcomment_create,
        'taskstatus': Dict_FeedbackTaskStatus.objects.filter(is_active=True),
        'tskstatus_selectid': tskstatus_selectid,
        'object_list': 'feedbacktask_list',
        'ticketcomment_costsum': ticketcomment_costsum,
        'task_costsum': task_costsum,
        'taskcomment_costsum': taskcomment_costsum,
        'taskcomment_timesum': taskcomment_timesum,
        'hours': hours, 'minutes': minutes, 'seconds': seconds,

    })

class FeedbackTicketCommentCreate(AddFilesMixin, CreateView):
    model = FeedbackTicketComment
    form_class = FeedbackTicketCommentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
        context = super(FeedbackTicketCommentCreate, self).get_context_data(**kwargs)
        context['header'] = 'Новый комментарий Тикета'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        is_support_member = self.request.session['_auth_user_issupportmember']
        kwargs.update({'is_support_member': is_support_member})
        return kwargs

    def form_valid(self, form):
        form.instance.ticket_id = self.kwargs['ticketid']
        form.instance.company_id = self.kwargs['companyid']
        #currentusercompanyid = request.session['_auth_user_currentcompany_id']
        #form.instance.company_id = currentusercompanyid
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новый коммент Тикета
        af = self.add_files(form, 'feedback', 'ticketcomment')  # добавляем файлы из формы (метод из AddFilesMixin)
        return super().form_valid(form)

class FeedbackTaskCreate(AddFilesMixin, CreateView):
    model = FeedbackTask
    form_class = FeedbackTaskForm
    # template_name = 'task_create.html'
    template_name = 'object_form.html'

    def form_valid(self, form):
        form.instance.ticket_id = self.kwargs['ticketid']
        if self.kwargs['parentid'] != 0:
            form.instance.parent_id = self.kwargs['parentid']
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новую задачу Тикета
        af = self.add_files(form, 'feedback', 'task')  # добавляем файлы из формы (метод из AddFilesMixin)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FeedbackTaskCreate, self).get_context_data(**kwargs)
        context['header'] = 'Новая Задача'
        return context

    def get_form_kwargs(self):
        kwargs = super(FeedbackTaskCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user, 'action': 'create', 'ticketid': self.kwargs['ticketid']})
        return kwargs


class FeedbackTaskUpdate(AddFilesMixin, UpdateView):
    model = FeedbackTask
    form_class = FeedbackTaskForm
    # template_name = 'task_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
        context = super(FeedbackTaskUpdate, self).get_context_data(**kwargs)
        context['header'] = 'Изменить Задачу'
        context['files'] = FeedbackFile.objects.filter(task_id=self.kwargs['pk'], is_active=True).order_by('uname')
        return context

    def get_form_kwargs(self):
        kwargs = super(FeedbackTaskUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user, 'action': 'update'})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        af = self.add_files(form, 'feedback', 'task')  # добавляем файлы из формы (метод из AddFilesMixin)
        old = FeedbackTask.objects.filter(
            pk=self.object.pk).first()  # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта

        return super().form_valid(form)


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def feedbacktaskcomments(request, taskid):
    currenttask = FeedbackTask.objects.filter(id=taskid).first()
    currentuser = request.user.id
    if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id:
        obj_files_rights = 1
    else:
        obj_files_rights = 0

    #taskcomment_costsum = FeedbackTaskComment.objects.filter(task=taskid).aggregate(Sum('cost'))
    #taskcomment_timesum = FeedbackTaskComment.objects.filter(task=taskid).aggregate(Sum('time'))
    taskcomment_costsum = currenttask.costsum
    taskcomment_timesum = currenttask.timesum

    try:
        sec = taskcomment_timesum["time__sum"] * 3600
    except:
        sec = 0
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    seconds = sec
    taskcomment_list = FeedbackTaskComment.objects.filter(Q(author=request.user.id), is_active=True, task=taskid)

    #event_list = ClientEvent.objects.filter(task=currenttask, is_active=True)

    # print(taskcomment_list)
    button_taskcomment_create = ''
    # button_taskcomment_update = ''
    button_task_create = ''
    button_task_update = ''
    button_task_history = ''
    #print(currentuser, currenttask.author_id, currenttask.assigner_id)
    if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id: # or is_member:
        button_task_create = 'Добавить'
        #button_task_history = 'История'
        button_taskcomment_create = 'Добавить'
        if currentuser == currenttask.author_id or currentuser == currenttask.assigner_id:
            button_task_update = 'Изменить'

    return render(request, "feedbacktask_detail.html", {
        'nodes': taskcomment_list.distinct().order_by(),
        # 'current_taskcomment': currenttaskcomment,
        'task': currenttask,
        'obj_files_rights': obj_files_rights,
        'files': FeedbackFile.objects.filter(task=currenttask, is_active=True).order_by('uname'),
        'objtype': 'fbtsk',
        'button_task_create': button_task_create,
        'button_task_update': button_task_update,
        #'button_task_history': button_task_history,
        #'object_list': 'clienttask_list',
        'taskcomment_costsum': taskcomment_costsum,
        'taskcomment_timesum': taskcomment_timesum,
        'hours': hours, 'minutes': minutes, 'seconds': seconds,
        'button_taskcomment_create': button_taskcomment_create,
        #'enodes': event_list.distinct().order_by(),
        #'button_event_create': button_event_create,
        'media_path': settings.MEDIA_URL,
    })


class FeedbackTaskCommentDetail(DetailView):
    model = FeedbackTaskComment
    template_name = 'taskcomment_detail.html'


class FeedbackTaskCommentCreate(AddFilesMixin, CreateView):
    model = FeedbackTaskComment
    form_class = FeedbackTaskCommentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
        context = super(FeedbackTaskCommentCreate, self).get_context_data(**kwargs)
        context['header'] = 'Новый Комментарий'
        return context

    def form_valid(self, form):
        form.instance.task_id = self.kwargs['taskid']
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новый коммент задачи клиента
        af = self.add_files(form, 'feedback', 'taskcomment')  # добавляем файлы из формы (метод из AddFilesMixin)
        return super(FeedbackTaskCommentCreate, self).form_valid(form)


class FeedbackTaskCommentUpdate(UpdateView):
    model = FeedbackTaskComment
    #form_class = FeedbackTaskCommentForm
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
        context = super(FeedbackTaskCommentUpdate, self).get_context_data(**kwargs)
        context['header'] = 'Изменить Комментарий'
        context['files'] = FeedbackFile.objects.filter(taskcomment_id=self.kwargs['pk'], is_active=True).order_by('uname')
        return context


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def ticketfilter(request):

        companyid = request.GET['companyid']
        statusid = request.GET['statusid']
        typeid = request.GET['typeid']
        mytskuser = request.GET['my']

        currentuser = request.user.id
        current_company = Company.objects.filter(id=companyid).first()
        if companyid == 0:
            companyid = request.session['_auth_user_currentcompany_id']

        ticket_list = FeedbackTicket.objects.filter(is_active=True, company_id=companyid)

        # *** фильтруем по статусу ***
        if statusid == "0":
            ticket_list = ticket_list.filter(dateclose__isnull=True)
        elif statusid == "-2":
            ticket_list = ticket_list.filter(dateclose__lte=datetime.now())
        elif statusid != "-1":
            ticket_list = ticket_list.filter(status_id=statusid)

        # *** фильтруем по типу ***
        if typeid != "-1":
            ticket_list = ticket_list.filter(type_id=typeid)
        # *** фильтр по принадлежности ***
        if mytskuser == "1":
            #ticket_list = ticket_list.filter(author_id=currentuser)
            ticket_list = ticket_list.filter(Q(author=request.user.id))
        # **********
        #print(companyid, currentuser, statusid, typeid, my)
        nodes = ticket_list.distinct() #.order_by()
        #print(ticket_list, nodes)
        #status_list = ticket_list.values('status_id')
        #ticketstatus = Dict_FeedbackTicketStatus.objects.filter(id__in=status_list)
        #types_list = ticket_list.values('type_id')
        #tickettype = Dict_FeedbackTicketType.objects.filter(id__in=types_list)
        ticketstatus = Dict_FeedbackTicketStatus.objects.filter(is_active=True)
        tickettype = Dict_FeedbackTicketType.objects.filter(is_active=True)
        #print(statuss_list, ticketstatus)

        button_feedbackticket_create = 'Добавить'

        len_list = len(nodes)
        object_message = ''
        if len_list == 0:
           object_message = 'Тикеты не найдены!'

        return render(request, 'feedbacktickets_list.html', {'nodes_tickets': nodes,
                                                             'object_list': 'feedbacktask_list',
                                                             'len_list': len_list,
                                                             'current_company': current_company,
                                                             'current_ticketid': 0,
                                                             'object_message': object_message,
                                                             'ticketstatus': ticketstatus,
                                                             'tickettype': tickettype,
                                                             'myticketselectid': mytskuser,
                                                             'button_feedbackticket_create': button_feedbackticket_create,
                                                            }
                      )


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def tickettaskfilter(request):

        companyid = request.GET['companyid']
        ticketid = request.GET['ticketid']
        statusid = request.GET['statusid']
        mytskuser = request.GET['my']

        #currentuser = request.user.id
        current_company = Company.objects.filter(id=companyid).first()
        if companyid == "0":
            companyid = request.session['_auth_user_currentcompany_id']
        #current_ticket = ''
        if ticketid == "0":
            tickettask_list = FeedbackTask.objects.filter(is_active=True, ticket__company_id=companyid)
            current_ticketid = 0
        else:
            current_ticket = FeedbackTicket.objects.filter(id=ticketid).first()
            current_ticketid = current_ticket.id
            tickettask_list = FeedbackTask.objects.filter(is_active=True, ticket_id=ticketid)

        # *** фильтруем по статусу ***
        if statusid == "0":
            tickettask_list = tickettask_list.filter(dateclose__isnull=True)
        elif statusid == "-2":
            tickettask_list = tickettask_list.filter(dateclose__isnull=True, dateend__lte=datetime.now())
        elif statusid != "-1":
            tickettask_list = tickettask_list.filter(status_id=statusid)
        # **********

        # *** фильтр по принадлежности ***
        if mytskuser == "1":
            tickettask_list = tickettask_list.filter(Q(author=request.user.id))
        elif mytskuser == "2":
            tickettask_list = tickettask_list.filter(Q(assigner=request.user.id))
        # *******************************

        nodes = tickettask_list.distinct() #.order_by()
        taskstatus = Dict_FeedbackTaskStatus.objects.filter(is_active=True)

        len_list = len(nodes)
        object_message = ''
        if len_list == 0:
           object_message = 'Задачи не найдены!'

        return render(request, 'objects_list.html', {'nodes': nodes,
                                                           'current_company': current_company,
                                                           'current_ticketid': current_ticketid,
                                                           'len_list': len_list,
                                                           'object_message': object_message,
                                                           'taskstatus': taskstatus,
                                                           'mytickettaskselectid': mytskuser,
                                                          }
                      )
