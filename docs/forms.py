from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget

from django import forms
from .models import Company, Doc, DocTask, DocTaskComment
from .models import Dict_DocStatus, Dict_DocType
from main.models import Notification, Meta_ObjectType
from accounts.models import UserProfile
from companies.models import UserCompanyComponentGroup
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.context_processors import auth
import datetime
from django.conf import settings
from django.core.mail import send_mail


class DocForm(forms.ModelForm):

    files = forms.FileField(label='Файлы документа', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    disabled_fields = ('datepublic', 'author',)
    #disabled_fields = ('datecreate', 'author',)

    def clean(self):

        if self.action == 'update':
           if self.cleaned_data['status'].id != self.initial['status']:
              # если вызов пришёл из DocUpdate и статус Документа был изменён, то пишем лог изменения
              #dict_status = Dict_DocStatus.objects.get(pk=self.cleaned_data['status'].id)
              #DocStatusLog.objects.create(doc_id=self.initial['id'],
              #                                status_id=dict_status.id,
              #                                author_id=self.user.id)
              if self.cleaned_data['status'].is_public:
                 '''
                 if self.user.id != self.initial['author']:
                    # если Документ публикуется Менеджером, то уведомление отсылается Автору
                    self.cleaned_data['datepublic'] = datetime.datetime.today()
                    #self.cleaned_data['percentage'] = 100
                    #self.cleaned_data['phone'] = '+7(999)999-9998'
                    ##user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                    user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                    objecttypeid = Meta_ObjectType.objects.get(shortname='doc').id
                    send_mail('1YES! Ваш Документ опубликован.', 'Уведомляем о публикации Вашего Документа!', settings.EMAIL_HOST_USER, [user_profile.email])
                    Notification.objects.create(type=user_profile.protocoltype,
                                                objecttype_id=objecttypeid,
                                                objectid=self.initial['id'],
                                                sendfrom=settings.EMAIL_HOST_USER,
                                                theme='Ваш Документ опубликован!',
                                                text='Уведомляем об опубликовании Вашего Документа.',
                                                recipient_id=self.initial['author'],
                                                sendto=user_profile.email,
                                                author_id=self.user.id)
                 '''
              else:
                 self.cleaned_data['datepublic'] = None
           elif self.cleaned_data['manager'].id != self.initial['manager']:
              user_profile = UserProfile.objects.get(user=self.cleaned_data['manager'].id, is_active=True)
              objecttypeid = Meta_ObjectType.objects.get(shortname='doc').id
              send_mail('1YES! Вы назначены менеджером Документа.', 'Уведомляем о назначении Вам Документа!', settings.EMAIL_HOST_USER, [user_profile.email])
              Notification.objects.create(type=user_profile.protocoltype,
                                          objecttype_id=objecttypeid,
                                          objectid=self.initial['id'],
                                          sendfrom=settings.EMAIL_HOST_USER,
                                          theme='Вы назначены менеджером Документа.',
                                          text='Уведомляем о назначении Вам Документа "'+self.cleaned_data['name']+'".',
                                          recipient_id=self.initial['manager'],
                                          sendto=user_profile.email,
                                          author_id=self.user.id)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму

        if self.action == 'create':
           self.company = kwargs.pop('companyid')
           super().__init__(*args, **kwargs)
           companyid = self.company
        else:
           super().__init__(*args, **kwargs)
           companyid = self.instance.company_id
           # Менеджер не может менять Менеджера
           if self.user.id == self.initial['manager']:
              self.fields['manager'].disabled = True

        # в выпадающие списки для выбора Менеджера и Участников Документа подбираем только тех юзеров, которые привязаны к этой организации (в админке)
        uc = UserCompanyComponentGroup.objects.filter(company_id=companyid).values_list('user_id', flat=True)
        usr = User.objects.filter(id__in=uc, is_active=True)
        self.fields['manager'].queryset = usr
        self.fields['members'].queryset = usr
        self.fields['author'].initial = self.user.id

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Doc
        fields = ['name', 'description', 'manager', 'type', 'status', 'members', 'datepublic', 'is_active', 'id', 'author']
        #widgets = {
        #    'datebegin': DatePickerInput(format='%d.%m.%Y'), # default date-format %m/%d/%Y will be used
        #    'dateend': DatePickerInput(format='%d.%m.%Y'), # specify date-frmat
        #}

class DocTaskForm(forms.ModelForm):

    files = forms.FileField(label='Файлы задачи', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    disabled_fields = ('dateclose', 'author',)

    def clean(self):
        if self.cleaned_data['dateend'] < self.cleaned_data['datebegin']:
           self.cleaned_data['dateend'] = self.cleaned_data['datebegin']
        # здесь надо поставить проверку на view.TaskUpdate
        if self.action == 'update':
           if self.cleaned_data['status'].id != self.initial['status']:
              # если вызов пришёл из TaskUpdate и статус задачи был изменён, то пишем лог изменения (это переехало в переопределение метода save в модели)
              #dict_status = Dict_ClientTaskStatus.objects.get(pk=self.cleaned_data['status'].id)
              #ClientTaskStatusLog.objects.create(task_id=self.initial['id'],
              #                                   status_id=dict_status.id,
              #                                   author_id=self.user.id)
              if self.cleaned_data['status'].is_close:
                 if self.user.id != self.initial['author']:
                    self.cleaned_data['dateclose'] = datetime.datetime.today()
                    self.cleaned_data['percentage'] = 100
                    #user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                    user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                    objecttypeid = Meta_ObjectType.objects.get(shortname='tsk').id
                    send_mail('1YES! Ваша Задача закрыта.', 'Уведомляем о закрытии Вашей Задачи!', settings.EMAIL_HOST_USER, [user_profile.email])
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
              send_mail('1YES! Вы назначены исполнителем Задачи.', 'Уведомляем о назначении Вам Задачи!', settings.EMAIL_HOST_USER, [user_profile.email])
              Notification.objects.create(type=user_profile.protocoltype,
                                          objecttype_id=objecttypeid,
                                          objectid=self.initial['id'],
                                          sendfrom=settings.EMAIL_HOST_USER,
                                          theme='Вы назначены исполнителем Задачи.',
                                          text='Уведомляем о назначении Вам Задачи "'+self.cleaned_data['name']+'".',
                                          recipient_id=self.cleaned_data['assigner'],
                                          sendto=user_profile.email,
                                          author_id=self.user.id)

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму
        #self.is_event = kwargs.pop('is_event')  # Узнаём, что за модель
        #is_event = bool(self.is_event)

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
        #print(members_list)
        # в выпадающий список для выбора Исполнителя Задачи подбираем только тех юзеров, которые являются участниками этого Клиента
        usr = User.objects.filter(id__in=members_list, is_active=True)
        #print (usr)
        self.fields['assigner'].queryset = usr
        self.fields['author'].initial = self.user.id
        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = DocTask
        fields = ['name', 'description', 'assigner', 'dateend', 'type', 'status', 'dateclose', 'is_active', 'id', 'author']
        widgets = {
            'datebegin': DatePickerInput(format='%d.%m.%Y %H:%M'), # default date-format %m/%d/%Y will be used
            'dateend': DatePickerInput(format='%d.%m.%Y %H:%M'), # specify date-frmat
        }