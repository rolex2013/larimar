from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Company, Client, ClientTask, ClientTaskComment, ClientEvent, ClientEventComment
#from .models import ClientStatusLog, ClientTaskStatusLog, ClientEventStatusLog
from .models import Dict_ClientStatus, Dict_ClientType, Dict_ClientTaskStatus, Dict_ClientEventType, Dict_ClientEventStatus
from main.models import Notification, Meta_ObjectType
from accounts.models import UserProfile
from companies.models import UserCompanyComponentGroup
from django.contrib.auth.models import User
#from django.contrib.admin.widgets import AdminDateWidget
#from django.contrib.admin.widgets import AdminSplitDateTime
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.contrib.auth.context_processors import auth
import datetime
from django.conf import settings
from django.core.mail import send_mail

from django.utils.translation import gettext_lazy as _


class ClientForm(forms.ModelForm):

    # хотелось бы, если выбран юзер, заполнять данные этой формы (ФИО, email, phone) из его Профиля

    files = forms.FileField(label=_('Файлы клиента'), widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    disabled_fields = ('dateclose', 'author',)

    def clean(self):

        if self.action == 'update':
            if self.cleaned_data['status'].id != self.initial['status']:
                if self.cleaned_data['status'].is_close: # == "Выполнен":
                    if self.user.id != self.initial['author']:
                        # если Клиент закрывается Менеджером, то уведомление отсылается Автору
                        self.cleaned_data['dateclose'] = datetime.datetime.today()
                        # self.cleaned_data['percentage'] = 100
                        # self.cleaned_data['phone'] = '+7(999)999-9998'
                        # #user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                        user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                        objecttypeid = Meta_ObjectType.objects.get(shortname='clnt').id
                        send_mail(_('1YES! Ваш Клиент закрыт.'), _('Уведомляем о закрытии Вашего Клиента!'), settings.EMAIL_HOST_USER, [user_profile.email])
                        Notification.objects.create(type=user_profile.protocoltype,
                                                    objecttype_id=objecttypeid,
                                                    objectid=self.initial['id'],
                                                    sendfrom=settings.EMAIL_HOST_USER,
                                                    theme=_('Ваш Клиент закрыт!'),
                                                    text=_('Уведомляем о закрытии Вашего Клиента.'),
                                                    recipient_id=self.initial['author'],
                                                    sendto=user_profile.email,
                                                    author_id=self.user.id)
                else:
                    self.cleaned_data['dateclose'] = None
            elif self.cleaned_data['manager'].id != self.initial['manager']:
                user_profile = UserProfile.objects.get(user=self.cleaned_data['manager'].id, is_active=True)
                objecttypeid = Meta_ObjectType.objects.get(shortname='clnt').id
                send_mail(_('1YES! Вы назначены менеджером Клиента.'), _('Уведомляем о назначении Вам Клиента!'), settings.EMAIL_HOST_USER, [user_profile.email])
                Notification.objects.create(type=user_profile.protocoltype,
                                            objecttype_id=objecttypeid,
                                            objectid=self.initial['id'],
                                            sendfrom=settings.EMAIL_HOST_USER,
                                            theme=_('Вы назначены менеджером Клиента.'),
                                            text=_('Уведомляем о назначении Вам Клиента "')+self.cleaned_data['firstname']+' '+self.cleaned_data['middlename']+' '+self.cleaned_data['lastname']+'".',
                                            recipient_id=self.initial['manager'],
                                            sendto=user_profile.email,
                                            author_id=self.user.id)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму

        if self.action == 'create':
            self.company = kwargs.pop('companyid')
            super(ClientForm, self).__init__(*args, **kwargs)
            companyid = self.company
        else:
            super(ClientForm, self).__init__(*args, **kwargs)
            companyid = self.instance.company_id
            # Менеджер не может менять Менеджера
            if self.user.id == self.initial['manager']:
                self.fields['manager'].disabled = True

        # в выпадающие списки для выбора Менеджера (Руководителя) и участников Клиента подбираем только тех юзеров, которые привязаны к этой организации (в админке)
        uc = UserCompanyComponentGroup.objects.filter(company_id=companyid).values_list('user_id', flat=True)
        usr = User.objects.filter(id__in=uc, is_active=True)
        self.fields['manager'].queryset = usr
        self.fields['members'].queryset = usr
        self.fields['author'].initial = self.user.id

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Client
        fields = ['user', 'firstname', 'middlename', 'lastname', 'description', 'phone', 'email', 'members', 'manager', 'type', 'status', 'currency', 'cost', 'percentage', 'dateclose', 'is_notify', 'protocoltype', 'initiator', 'is_active', 'id', 'author']
        # widgets = {
        #    'datebegin': DatePickerInput(format='%d.%m.%Y'), # default date-format %m/%d/%Y will be used
        #    'dateend': DatePickerInput(format='%d.%m.%Y'), # specify date-format
        # }


class ClientTaskForm(forms.ModelForm):

    files = forms.FileField(label=_('Файлы задачи'), widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    disabled_fields = ('dateclose', 'author',)

    def clean(self):
        if self.cleaned_data['dateend'] < self.cleaned_data['datebegin']:
            self.cleaned_data['dateend'] = self.cleaned_data['datebegin']
        # здесь надо поставить проверку на view.TaskUpdate
        if self.action == 'update':
            if self.cleaned_data['status'].id != self.initial['status']:

                if self.cleaned_data['status'].is_close:
                    if self.user.id != self.initial['author']:
                        self.cleaned_data['dateclose'] = datetime.datetime.today()
                        self.cleaned_data['percentage'] = 100
                        # user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                        user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                        objecttypeid = Meta_ObjectType.objects.get(shortname='tsk').id
                        send_mail(_('1YES! Ваша Задача закрыта.'), _('Уведомляем о закрытии Вашей Задачи!'), settings.EMAIL_HOST_USER, [user_profile.email])
                        Notification.objects.create(type=user_profile.protocoltype,
                                                    objecttype_id=objecttypeid,
                                                    objectid=self.initial['id'],
                                                    sendfrom=settings.EMAIL_HOST_USER,
                                                    theme=_('Ваша Задача закрыта.'),
                                                    text=_('Уведомляем о закрытии Вашей Задачи!'),
                                                    recipient_id=self.initial['author'],
                                                    sendto=user_profile.email,
                                                    author_id=self.user.id)
                else:
                    self.cleaned_data['dateclose'] = None
            elif self.cleaned_data['assigner'].id != self.initial['assigner']:
                user_profile = UserProfile.objects.get(user=self.cleaned_data['assigner'].id, is_active=True)
                objecttypeid = Meta_ObjectType.objects.get(shortname='tsk').id
                send_mail(_('1YES! Вы назначены исполнителем Задачи.'), _('Уведомляем о назначении Вам Задачи!'), settings.EMAIL_HOST_USER, [user_profile.email])
                Notification.objects.create(type=user_profile.protocoltype,
                                            objecttype_id=objecttypeid,
                                            objectid=self.initial['id'],
                                            sendfrom=settings.EMAIL_HOST_USER,
                                            theme=_('Вы назначены исполнителем Задачи.'),
                                            text=_('Уведомляем о назначении Вам Задачи "')+self.cleaned_data['name']+'".',
                                            recipient_id=self.cleaned_data['assigner'],
                                            sendto=user_profile.email,
                                            author_id=self.user.id)

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму
        # self.is_event = kwargs.pop('is_event')  # Узнаём, что за модель
        # is_event = bool(self.is_event)

        if self.action == 'create':
            self.client = kwargs.pop('clientid')
            super(ClientTaskForm, self).__init__(*args, **kwargs)
            clnt = Client.objects.get(id=self.client)
            companyid = clnt.company_id
        else:
            super(ClientTaskForm, self).__init__(*args, **kwargs)
            companyid = self.instance.client.company_id
            self.client = self.instance.client_id
            # Исполнитель не может менять Исполнителя
            if self.user.id == self.initial['assigner']:
                self.fields['assigner'].disabled = True

        # выцепляем id юзеров-участников Клиента
        members_list = list(Client.objects.filter(id=self.client).values_list('members', flat=True))
        # print(members_list)
        # в выпадающий список для выбора Исполнителя Задачи подбираем только тех юзеров, которые являются участниками этого Клиента
        usr = User.objects.filter(id__in=members_list, is_active=True)
        # print (usr)
        self.fields['assigner'].queryset = usr
        self.fields['author'].initial = self.user.id
        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = ClientTask
        fields = ['name', 'description', 'assigner', 'datebegin', 'dateend', 'structure_type', 'type', 'status', 'cost', 'percentage', 'initiator', 'dateclose', 'is_active', 'id', 'author']
        widgets = {
            'datebegin': DateTimePickerInput(options={'format': 'DD.MM.YY HH:MM'}), # default date-format %m/%d/%Y will be used
            'dateend': DateTimePickerInput(options={'format': 'DD.MM.YY HH:MM'}), # specify date-frmat
        }


class ClientTaskCommentForm(forms.ModelForm):

    files = forms.FileField(label=_('Файлы комментария задачи'), widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = ClientTaskComment
        fields = ['name', 'description', 'time', 'cost']


class FilterStatusForm(forms.ModelForm):

    class Meta:
        model = Dict_ClientStatus
        fields = ['name_ru', 'name_en']


class ClientEventForm(forms.ModelForm):

    files = forms.FileField(label='Файлы события', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    disabled_fields = ('dateclose', 'author',)

    def clean(self):

        if self.cleaned_data['dateend'] < self.cleaned_data['datebegin']:
            self.cleaned_data['dateend'] = self.cleaned_data['datebegin']
        # здесь надо поставить проверку на view.EventUpdate
        if self.action == 'update':

            if self.cleaned_data['status'].id != self.initial['status']:

                if self.cleaned_data['status'].is_close:
                    if self.user.id != self.initial['author']:
                        self.cleaned_data['dateclose'] = datetime.datetime.today()
                        user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                        objecttypeid = Meta_ObjectType.objects.get(shortname='evnt').id
                        send_mail(_('1YES! Ваша Задача закрыта.'), _('Уведомляем о закрытии Вашей Задачи!'), settings.EMAIL_HOST_USER, [user_profile.email])
                        Notification.objects.create(type=user_profile.protocoltype,
                                                    objecttype_id=objecttypeid,
                                                    objectid=self.initial['id'],
                                                    sendfrom=settings.EMAIL_HOST_USER,
                                                    theme='Ваше Событие закрыто.',
                                                    text='Уведомляем о закрытии Вашего События!',
                                                    recipient_id=self.initial['author'],
                                                    sendto=user_profile.email,
                                                    author_id=self.user.id)
                else:
                    self.cleaned_data['dateclose'] = None
                    
            elif self.cleaned_data['assigner'].id != self.initial['assigner']:
                user_profile = UserProfile.objects.get(user=self.cleaned_data['assigner'].id, is_active=True)
                objecttypeid = Meta_ObjectType.objects.get(shortname='tsk').id
                send_mail(_('1YES! Вы назначены исполнителем События.'), _('Уведомляем о назначении Вам События!'), settings.EMAIL_HOST_USER, [user_profile.email])
                Notification.objects.create(type=user_profile.protocoltype,
                                            objecttype_id=objecttypeid,
                                            objectid=self.initial['id'],
                                            sendfrom=settings.EMAIL_HOST_USER,
                                            theme=_('Вы назначены исполнителем События.'),
                                            text=_('Уведомляем о назначении Вам События "')+self.cleaned_data['name']+'".',
                                            recipient_id=self.cleaned_data['assigner'],
                                            sendto=user_profile.email,
                                            author_id=self.user.id)

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму

        if self.action == 'create':
            self.client = kwargs.pop('clientid')
            self.task = kwargs.pop('taskid')
            super(ClientEventForm, self).__init__(*args, **kwargs)
            clnt = Client.objects.get(id=self.client)
            companyid = clnt.company_id
            if self.task != 0:
                self.fields['task'].initial = self.task
        else:
            super(ClientEventForm, self).__init__(*args, **kwargs)
            companyid = self.instance.client.company_id
            self.client = self.instance.client_id
            # Исполнитель не может менять Исполнителя
            if self.user.id == self.initial['assigner']:
                self.fields['assigner'].disabled = True

        # выцепляем id юзеров-участников Клиента
        members_list = list(Client.objects.filter(id=self.client).values_list('members', flat=True))
        #print(members_list)
        # в выпадающий список для выбора Исполнителя События подбираем только тех юзеров, которые являются участниками этого Клиента
        usr = User.objects.filter(id__in=members_list, is_active=True)
        #print (usr)
        self.fields['assigner'].queryset = usr
        self.fields['author'].initial = self.user.id
        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = ClientEvent
        fields = ['name', 'description', 'assigner', 'datebegin', 'dateend', 'type', 'status', 'initiator', 'dateclose', 'task', 'is_active', 'id', 'author']
        widgets = {
            'datebegin': DateTimePickerInput(options={'format': 'DD.MM.YY HH:MM'}), # default date-format %m/%d/%Y will be used
            'dateend': DateTimePickerInput(options={'format': 'DD.MM.YY HH:MM'}), # specify date-frmat
        }


class ClientEventCommentForm(forms.ModelForm):

    files = forms.FileField(label=_('Файлы комментария события'),
                            widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            required=False)

    class Meta:
        model = ClientEventComment
        fields = ['name', 'description']
