from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from datetime import datetime, date, time

from rest_framework import viewsets

from .serializers import Dict_SystemSerializer, FeedbackTicketSerializer
from companies.models import Company, UserCompanyComponentGroup
from .models import Dict_System, Dict_FeedbackTicketStatus, Dict_FeedbackTicketType, Dict_FeedbackTaskStatus
from .models import FeedbackTicket, FeedbackTicketComment, FeedbackTask, FeedbackTaskComment
from .forms import FeedbackTicketForm #, TaskForm, TaskCommentForm

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

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def feedbacktickets(request, companyid=0, pk=0):

    currentuser = request.user.id
    currentusercompanyid = request.session['_auth_user_currentcompany_id']

    if companyid == 0:
        #companyid = request.session['_auth_user_currentcompany_id']
        mylastticket = FeedbackTicket.objects.filter(is_active=True, author_id=currentuser).order_by('-id')[0]
        companyid = mylastticket.company_id
    #print(companyid)

    request.session['_auth_user_currentcomponent'] = 'feedbacktickets'

    # Видимость пункта "- Все" в фильтрах
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
    print(is_support_member, is_support_admin_org, is_superadmin, is_admin_org, is_admin)

    # *** фильтруем по статусу ***
    tktstatus_selectid = 0
    #mytktstatus = 0 # для фильтра "Мои проекты"
    try:
       tktstatus = request.POST['select_feedbackticketstatus']
    except:
       feedbackticket_list = FeedbackTicket.objects.filter(Q(author=request.user.id), is_active=True, company=companyid, dateclose__isnull=True)
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

    len_list = len(feedbackticket_list)

    current_company = Company.objects.get(id=companyid)

    obj_files_rights = 0

    if pk == 0:
       current_feedbackticket = 0
    else:
       current_feedbackticket = FeedbackTicket.objects.get(id=pk)
       if currentuser == current_feedbackticket.author_id or currentuser == current_feedbackticket.assigner_id:
           obj_files_rights = 1

    button_company_select = ''
    button_feedbackticket_create = 'Добавить'

    comps = request.session['_auth_user_companies_id']

    # Проверяем кол-во компаний - служб техподдержки
    comps_support = Company.objects.filter(is_active=True, is_support=True)
    if len(comps_support) > 1:
       button_company_select = 'Сменить службу техподдержки'
    #if currentuser == current_company.author_id:
    #   button_feedbackticket_create = 'Добавить'
    #if current_company.id in comps:
    #   button_feedbackticket_create = 'Добавить'

    # Добавляем Систему в справочник
    dsys_cnt = Dict_System.objects.filter(is_active=True).count()
    if dsys_cnt == 0:
        #print(dsys_cnt)
        http_host = request.META['HTTP_HOST']
        #print(http_host)
        dsys = Dict_System.objects.create(code='===', name='1YES!', domain=http_host, url=http_host, is_active=True)
        dsys.save()

    return render(request, "company_detail.html", {
                              'nodes': feedbackticket_list.distinct(), #.order_by(), # для удаления задвоений и восстановления иерархии
                              'component_name': 'feedback',
                              'current_feedbackticket': current_feedbackticket,
                              'current_company': current_company,
                              'companyid': companyid,
                              'user_companies': comps,
                              'obj_files_rights': obj_files_rights,
                              'button_company_select': button_company_select,
                              'button_feedbackticket_create': button_feedbackticket_create,
                              'feedbackticketstatus': Dict_FeedbackTicketStatus.objects.filter(is_active=True),
                              'tktstatus_selectid': tktstatus_selectid,
                              #'tktstatus_myselectid': tktstatus_myselectid,
                              'object_list': 'feedbackticket_list',
                              #'select_feedbackticketstatus': select_feedbackticketstatus,
                              'len_list': len_list,
                              'is_support_member': is_support_member,
                              'is_admin': is_admin,
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
        # здесь нужно условие для 'action': 'create'
        kwargs.update({'user': self.request.user, 'action': 'create', 'systemid': self.kwargs['systemid'], 'companyid': self.kwargs['companyid']})
        return kwargs