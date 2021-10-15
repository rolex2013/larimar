from django.conf import settings
from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date, time
from django.db.models import Q, Count, Min, Max, Sum, Avg

from datetime import datetime, date, time

from rest_framework import viewsets

from .serializers import Dict_SystemSerializer, FeedbackTicketSerializer
from companies.models import Company, UserCompanyComponentGroup
from .models import Dict_System, Dict_FeedbackTicketStatus, Dict_FeedbackTicketType, Dict_FeedbackTaskStatus
from .models import FeedbackTicket, FeedbackTicketComment, FeedbackTask, FeedbackTaskComment, FeedbackFile
from .forms import FeedbackTicketForm, FeedbackTaskForm, FeedbackTicketCommentForm, FeedbackTaskCommentForm

from main.utils import AddFilesMixin


class Dict_SystemViewSet(viewsets.ModelViewSet):
    queryset = Dict_System.objects.all() #.order_by('name')
    serializer_class = Dict_SystemSerializer


class FeedbackTicketViewSet(viewsets.ModelViewSet):
    queryset = FeedbackTicket.objects.filter(is_active=True).order_by('-datecreate')
    serializer_class = FeedbackTicketSerializer
    #filter_fields = ('username', 'is_player', 'first_name', 'last_name', 'team', 'email',)

#def FeedbackTicketCreateAPI(request):
#    return

def definerights(request, companyid):
    currentuser = request.user.id
    currentusercompanyid = request.session['_auth_user_currentcompany_id']
    is_support_member = False
    is_support_admin_org = False
    is_superadmin = False
    is_admin_org = False
    is_admin = False
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
def feedbacktickets(request, companyid=0, pk=0):

    currentuser = request.user.id
    currentusercompanyid = request.session['_auth_user_currentcompany_id']

    if companyid == 0:

        try:
            mylastticket = FeedbackTicket.objects.filter(is_active=True, author_id=currentuser).order_by('-id')[0]
            companyid = mylastticket.company_id
        except:
            companyid = currentusercompanyid

        #print(companyid)

    request.session['_auth_user_currentcomponent'] = 'feedbacktickets'

    # Видимость пункта "- Все" в фильтрах
    (is_support_member, is_support_admin_org, is_admin_org, is_admin, is_superadmin) = definerights(request,companyid)

    request.session['_auth_user_issupportmember'] = is_support_member
    if is_support_member:
        request.session['_auth_user_supportcompany_id'] = companyid
    else:
        request.session['_auth_user_supportcompany_id'] = currentusercompanyid

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

    len_task_list = 0
    if is_support_member == True:
        feedbackticket_task_list = FeedbackTask.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id), is_active=True, ticket__company=companyid,
                                                        dateclose__isnull=True)
        len_task_list = len(feedbackticket_task_list)
        #print(len_task_list)

    len_list = len(feedbackticket_list)

    current_company = Company.objects.get(id=companyid)

    obj_files_rights = 0

    if pk == 0:
       current_feedbackticket = 0
    else:
       current_feedbackticket = FeedbackTicket.objects.get(id=pk)
       if currentuser == current_feedbackticket.author_id or currentuser == current_feedbackticket.assigner_id:
           obj_files_rights = 1

    comps = request.session['_auth_user_companies_id']

    # Заполняем списки справочников для фильтров
    # Статусы и Типы берём из списка тикетов всей компании
    all_list = FeedbackTicket.objects.filter(is_active=True, company=companyid)
    #status_list = feedbackticket_list.values('status_id')
    status_list = all_list.values('status_id')
    types_list = all_list.values('type_id')
    ticketstatus = Dict_FeedbackTicketStatus.objects.filter(id__in=status_list)
    tickettype = Dict_FeedbackTicketType.objects.filter(id__in=types_list)

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

        # Список всех задач этого сотрудника техподдержки
        task_list = FeedbackTask.objects.filter(
                            Q(author=request.user.id) | Q(assigner=request.user.id), ticket__company_id=currentusercompanyid,
                            is_active=True, dateclose__isnull=True)
    else:
        comps_support = Company.objects.filter(is_active=True, is_support=True)
        if len(comps_support) < 2:
            button_company_select = ''
        task_list = ''

    # Добавляем Систему в справочник
    dsys_cnt = Dict_System.objects.filter(is_active=True).count()
    if dsys_cnt == 0:
        #print(dsys_cnt)
        http_host = request.META['HTTP_HOST']
        #print(http_host)
        dsys = Dict_System.objects.create(code='===', name='1YES!', domain=http_host, url=http_host, is_active=True)
        dsys.save()

    return render(request, "company_detail.html", {
                              'nodes_tickets': feedbackticket_list.distinct(), #.order_by(), # для удаления задвоений и восстановления иерархии
                              'nodes': task_list, #.distinct(), #.order_by(),
                              'component_name': 'feedback',
                              'current_feedbackticket': current_feedbackticket,
                              'current_company': current_company,
                              'companyid': companyid,
                              'user_companies': comps,
                              'obj_files_rights': obj_files_rights,
                              'button_company_select': button_company_select,
                              'button_feedbackticket_create': button_feedbackticket_create,
                              'feedbackticketstatus': ticketstatus,
                              'feedbackticketstatus_selectid': '0',
                              'feedbacktickettype': tickettype,
                              'feedbacktickettype_selectid': '-1',
                              'feedbackticket_myselectid': '1',
                              #'tktstatus_myselectid': tktstatus_myselectid,
                              'object_list': 'feedbacktask_list',
                              #'select_feedbackticketstatus': select_feedbackticketstatus,
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
        'ticketid': ticketid,
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
        my = request.GET['my']
        currentuser = request.user.id
        current_company = Company.objects.filter(id=companyid).first()
        if companyid == 0:
            companyid = request.session['_auth_user_currentcompany_id']
        ticket_list = FeedbackTicket.objects.filter(is_active=True, company_id=companyid)
        # *** фильтруем по статусу ***
        if statusid == "0":
            ticket_list = ticket_list.filter(dateclose__isnull=True)
        elif statusid == "1":
            ticket_list = ticket_list.filter(dateclose__lte=datetime.now())
        # *** фильтруем по типу ***
        if typeid != "-1":
            ticket_list = ticket_list.filter(type_id=typeid)
        # *** фильтр по принадлежности ***
        if my == "1":
            ticket_list = ticket_list.filter(author_id=currentuser)
        # **********
        #print(currentuser, my)
        nodes = ticket_list.distinct() #.order_by()

        status_list = ticket_list.values('status_id')
        ticketstatus = Dict_FeedbackTicketStatus.objects.filter(id__in=status_list)
        types_list = ticket_list.values('type_id')
        tickettype = Dict_FeedbackTicketType.objects.filter(id__in=types_list)
        #print(statuss_list, ticketstatus)

        object_message = ''
        if len(nodes) == 0:
           object_message = 'Тикеты не найдены!'

        return render(request, 'feedbacktickets_list.html', {'nodes': nodes,
                                                     'current_company': current_company,
                                                     'object_message': object_message,
                                                     'ticketstatus': ticketstatus,
                                                     'tickettype': tickettype,
                                                     'myticketselectid': my,
                                                     }
                      )
