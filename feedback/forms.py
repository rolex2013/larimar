from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Company, FeedbackTicket, FeedbackTask, FeedbackTaskComment, FeedbackTicketComment, FeedbackFile
# from .models import FeedbackTicketStatusLog, TaskStatusLog
from .models import Dict_System, Dict_FeedbackTicketStatus, Dict_FeedbackTaskStatus
from main.models import Notification, Meta_ObjectType
from accounts.models import UserProfile
from companies.models import UserCompanyComponentGroup
from django.contrib.auth.models import User
# from django.contrib.admin.widgets import AdminDateWidget
# from django.contrib.admin.widgets import AdminSplitDateTime
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.contrib.auth.context_processors import auth
import datetime
from django.conf import settings
from django.core.mail import send_mail
 

class Dict_SystemForm(forms.ModelForm):
    # files = forms.FileField(label='Файлы комментария тикета', widget=forms.ClearableFileInput(attrs={'multiple': True}),
    #                        required=False)

    # def __init__(self, *args, **kwargs):
    #    self.is_support_member = kwargs.pop('is_support_member')
    #    super().__init__(*args, **kwargs)
    #    if not self.is_support_member:
    #        self.fields['time'].widget = forms.HiddenInput()
    #        self.fields['cost'].widget = forms.HiddenInput()

    class Meta:
        model = Dict_System
        # fields = ['name', 'domain', 'url', 'ip', 'email', 'phone']
        # fields = ['name', 'domain', 'url', 'email', 'phone']
        fields = ['name', 'domain', 'email', 'phone']


class FeedbackTicketForm(forms.ModelForm):
    # datebegin = forms.DateField(widget=AdminDateWidget())
    # datebegin = forms.DateField(widget=AdminSplitDateTime())

    files = forms.FileField(label='Файлы тикета', widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            required=False)
    # comment = forms.CharField(label='Комментарий', widget=CKEditorWidget(), required=False)
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea, required=False)

    # disabled_fields = ('name', 'description', 'type', 'files', 'status', 'is_active')
    # disabled_fields = ('dateclose', 'author')

    def clean(self):
        if self.action == 'update':
            if self.cleaned_data['status'].id != self.initial['status']:
                if self.cleaned_data['status'].is_close:  # Выполнен
                    self.cleaned_data['dateclose'] = datetime.datetime.today()
                    #self.cleaned_data['percentage'] = 100
                    #print(self.initial['author'])
                    if self.user.id != self.initial['author']:
                        # если Тикет закрывается Исполнителем из Службы Техподдержки, то уведомление отсылается Автору
                        # user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                        user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                        objecttypeid = Meta_ObjectType.objects.get(shortname='fbtkt').id
                        send_mail('1YES. Ваш Тикет закрыт.', 'Уведомляем о закрытии Вашего Тикета!',
                                  settings.EMAIL_HOST_USER, [user_profile.email])
                        # print('==================')
                else:
                    self.cleaned_data['dateclose'] = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop(
            'user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму
        self.is_support_member = kwargs.pop('is_support_member')
        self.is_system_dev = kwargs.pop('is_system_dev')

        if self.action == 'create':
            self.system = kwargs.pop('systemid')
            self.company = kwargs.pop('companyid')
            super().__init__(*args, **kwargs)
            companyid = self.company
            #systemid = self.system
            self.fields['comment'].widget = forms.HiddenInput()
            self.fields['author'].widget = forms.HiddenInput()
            self.fields['is_active'].disabled = True
        else:
            super().__init__(*args, **kwargs)
            companyid = self.instance.company_id
            #systemid = self.instance.system_id
            #for field in self.disabled_fields:
            #    self.fields[field].disabled = True
            #self.fields['author'].disabled = True
            self.fields['name'].disabled = True
            self.fields['description'].disabled = True
            self.fields['author'].widget = forms.HiddenInput()
            self.fields['files'].widget = forms.HiddenInput()
            #self.fields['name'].widget = forms.HiddenInput()
            #self.fields['description'].widget = forms.HiddenInput()

            #self.fields['type'].disabled = True
            if self.is_support_member:
                #if not self.is_system_dev:
                #    self.fields['files'].disabled = True
                self.fields['is_active'].disabled = True
            else:
                self.fields['status'].disabled = True

        #uc = UserCompanyComponentGroup.objects.filter(company_id=companyid).values_list('user_id', flat=True)
        #usr = User.objects.filter(id__in=uc, is_active=True)
        #self.fields['author'].initial = self.user.id

        #for field in self.disabled_fields:
        #    self.fields[field].disabled = True

    class Meta:
        model = FeedbackTicket
        fields = ['name', 'description', 'type', 'status', 'is_active', 'author']
        # labels = {'Files':'Выберите файлы'}
        widgets = {
            #'datebegin': DatePickerInput(format='%d.%m.%Y'),  # default date-format %m/%d/%Y will be used
            #'dateend': DatePickerInput(format='%d.%m.%Y')  # specify date-frmat,
            # 'docfile': forms.ClearableFileInput(attrs={'multiple': True}),
            # 'files': forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
        }

class FeedbackTicketCommentForm(forms.ModelForm):
    files = forms.FileField(label='Файлы комментария тикета', widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            required=False)

    def __init__(self, *args, **kwargs):
        self.is_support_member = kwargs.pop('is_support_member')
        self.is_ticketslist_dev = kwargs.pop('is_ticketslist_dev')
        print(self.is_ticketslist_dev)
        super().__init__(*args, **kwargs)
        if not self.is_support_member or self.is_ticketslist_dev == 1:
            self.fields['time'].widget = forms.HiddenInput()
            self.fields['cost'].widget = forms.HiddenInput()

    class Meta:
        model = FeedbackTicketComment
        fields = ['name', 'description', 'time', 'cost']

class FeedbackTaskForm(forms.ModelForm):
    files = forms.FileField(label='Файлы задачи', widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            required=False)

    disabled_fields = ('dateclose', 'author',)

    def clean(self):
        if self.cleaned_data['dateend'] < self.cleaned_data['datebegin']:
            self.cleaned_data['dateend'] = self.cleaned_data['datebegin']
        # здесь надо поставить проверку на view.TaskUpdate
        if self.action == 'update':
            if self.cleaned_data['status'].id != self.initial['status']:
                # если вызов пришёл из TaskUpdate и статус задачи был изменён, то пишем лог изменения (это переехало в переопределение метода save в модели)
                # dict_status = Dict_TaskStatus.objects.get(pk=self.cleaned_data['status'].id)
                # TaskStatusLog.objects.create(task_id=self.initial['id'],
                #                             status_id=dict_status.id,
                #                             author_id=self.user.id)
                if self.cleaned_data['status'].is_close:
                    if self.user.id != self.initial['author']:
                        self.cleaned_data['dateclose'] = datetime.datetime.today()
                        self.cleaned_data['percentage'] = 100
                        # user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                        user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                        objecttypeid = Meta_ObjectType.objects.get(shortname='tsk').id
                        send_mail('1Yes. Ваша Задача закрыта.', 'Уведомляем о закрытии Вашей Задачи!',
                                  settings.EMAIL_HOST_USER, [user_profile.email])
                        Notification.objects.create(type=user_profile.protocoltype,
                                                    objecttype_id=objecttypeid,
                                                    objectid=self.initial['id'],
                                                    sendfrom=settings.EMAIL_HOST_USER,
                                                    theme='Ваша Задача закрыта.',
                                                    text='Уведомляем о закрытии Вашей Задачи!',
                                                    recipient_id=self.initial['author'],
                                                    sendto=user_profile.email,
                                                    author_id=self.user.id)
                else:
                    self.cleaned_data['dateclose'] = None
            elif self.cleaned_data['assigner'].id != self.initial['assigner']:
                user_profile = UserProfile.objects.get(user=self.cleaned_data['assigner'].id, is_active=True)
                objecttypeid = Meta_ObjectType.objects.get(shortname='tsk').id
                send_mail('1Yes. Вы назначены исполнителем Задачи.', 'Уведомляем о назначении Вам Задачи!',
                          settings.EMAIL_HOST_USER, [user_profile.email])
                Notification.objects.create(type=user_profile.protocoltype,
                                            objecttype_id=objecttypeid,
                                            objectid=self.initial['id'],
                                            sendfrom=settings.EMAIL_HOST_USER,
                                            theme='Вы назначены исполнителем Задачи.',
                                            text='Уведомляем о назначении Вам Задачи "' + self.cleaned_data[
                                                'name'] + '".',
                                            recipient_id=self.cleaned_data['assigner'],
                                            sendto=user_profile.email,
                                            author_id=self.user.id)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop(
            'user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму
        if self.action == 'create':
            self.ticket = kwargs.pop('ticketid')
            companyid = kwargs.pop('companyid')
            super().__init__(*args, **kwargs)
            #tkt = FeedbackTicket.objects.filter(id=self.ticket).first()
            #companyid = tkt.company_id
        else:
            super().__init__(*args, **kwargs)
            companyid = self.instance.ticket.company_id
            self.ticket = self.instance.ticket_id
            # Исполнитель не может менять Исполнителя, если он не Автор
            if self.user.id == self.initial['assigner'] and self.initial['assigner'] != self.initial['author']:
                self.fields['assigner'].disabled = True
        # в выпадающий список для выбора Исполнителя подбираем только тех юзеров, которые привязаны к этой организации (в админке)
        uc = UserCompanyComponentGroup.objects.filter(is_active=True, company_id=companyid).values_list('user_id', flat=True)
        usr = User.objects.filter(id__in=uc, is_active=True)
        #usr = User.objects.filter(id__in=usr, is_active=True)
        self.fields['assigner'].queryset = usr
        self.fields['author'].initial = self.user.id

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = FeedbackTask
        fields = ['name', 'description', 'assigner', 'cost', 'datebegin', 'dateend', 'status',
                  'percentage', 'is_active', 'dateclose', 'id', 'author']
        widgets = {
            'datebegin': DateTimePickerInput(options={'format': 'DD.MM.YY HH:MM'}),
            'dateend': DateTimePickerInput(options={'format': 'DD.MM.YY HH:MM'}),
        }


class FeedbackTaskCommentForm(forms.ModelForm):
    files = forms.FileField(label='Файлы комментария', widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            required=False)

    class Meta:
        model = FeedbackTaskComment
        fields = ['name', 'description', 'time', 'cost']


class FilterStatusForm(forms.ModelForm):
    class Meta:
        model = Dict_FeedbackTicketStatus
        fields = ['name_ru', 'name_en']

#
# class DateForm(forms.Form):
#    date = forms.DateTimeField(
#        input_formats=['%d/%m/%Y %H:%M'],
#        widget=forms.DateTimeInput(attrs={
#            'class': 'form-control datetimepicker-input',
#            'data-target': '#datetimepicker1'
#        })
#    )