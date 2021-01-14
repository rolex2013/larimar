from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Company, Client #, ClientTask, ClientTaskComment
#from .models import ClientStatusLog, ClientTaskStatusLog
from .models import Dict_ClientStatus, Dict_ClientType #,Dict_ClientTaskStatus
from main.models import Notification, Meta_ObjectType
from accounts.models import UserProfile
from companies.models import UserCompanyComponentGroup
from django.contrib.auth.models import User
#from django.contrib.admin.widgets import AdminDateWidget
#from django.contrib.admin.widgets import AdminSplitDateTime
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.context_processors import auth
import datetime
from django.conf import settings
from django.core.mail import send_mail


class ClientForm(forms.ModelForm):
    #datebegin = forms.DateField(widget=AdminDateWidget())
    #datebegin = forms.DateField(widget=AdminSplitDateTime())

    # хотелось бы, если выбран юзер, заполнять данные этой формы (ФИО, email, phone) из его Профиля

    disabled_fields = ('dateclose', 'author',)

    def clean(self):
        #if self.cleaned_data['dateend'] < self.cleaned_data['datebegin']:
        #   self.cleaned_data['dateend'] = self.cleaned_data['datebegin']
        if self.action == 'update': 
           if self.cleaned_data['status'].id != self.initial['status']:
              # если вызов пришёл из ClientUpdate и статус Клиента был изменён, то пишем лог изменения 
              dict_status = Dict_ClientStatus.objects.get(pk=self.cleaned_data['status'].id)
              #ClientStatusLog.objects.create(project_id=self.initial['id'], 
              #                                status_id=dict_status.id, 
              #                                author_id=self.user.id)
              if self.cleaned_data['status'].is_close: # == "Выполнен":
                 if self.user.id != self.initial['author']: 
                    # если Клиент закрывается Менеджером, то уведомление отсылается Автору
                    self.cleaned_data['dateclose'] = datetime.datetime.today()
                    #self.cleaned_data['percentage'] = 100  
                    #self.cleaned_data['phone'] = '+7(999)999-9998'
                    ##user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)    
                    user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                    objecttypeid = Meta_ObjectType.objects.get(shortname='clnt').id                                       
                    #send_mail('LarimarITGroup. Ваш Проект закрыт.', 'Уведомляем о закрытии Вашего Проекта!', settings.EMAIL_HOST_USER, [user_profile.email])
                    Notification.objects.create(type=user_profile.protocoltype,
                                                objecttype_id=objecttypeid,
                                                objectid=self.initial['id'],
                                                sendfrom=settings.EMAIL_HOST_USER,
                                                theme='Ваш Клиент переведён в статус "'+dict_status.name+'"',
                                                text='Уведомляем об изменении статуса Вашего Клиента "'+self.cleaned_data['name']+'".',
                                                recipient_id=self.initial['author'],                                             
                                                sendto=user_profile.email,
                                                author_id=self.user.id)
              else:
                 self.cleaned_data['dateclose'] = None
           elif self.cleaned_data['assigner'].id != self.initial['assigner']:
              user_profile = UserProfile.objects.get(user=self.cleaned_data['assigner'].id, is_active=True)
              objecttypeid = Meta_ObjectType.objects.get(shortname='prj').id
              #send_mail('LarimarITGroup. Вы назначены менеджерои Клиента.', 'Уведомляем о назначении Вам Клиента!', settings.EMAIL_HOST_USER, [user_profile.email])
              Notification.objects.create(type=user_profile.protocoltype,
                                          object_id=objecttypeid,  
                                          objectid=self.initial['id'],            
                                          sendfrom=settings.EMAIL_HOST_USER,
                                          theme='Вы назначены менеджером Клиента.',
                                          text='Уведомляем о назначении Вам Клиента "'+self.cleaned_data['name']+'".',
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
        fields = ['user', 'firstname', 'middlename', 'lastname', 'description', 'phone', 'email', 'members', 'manager', 'type', 'status', 'dateclose', 'is_notify', 'protocoltype', 'is_active', 'id', 'author']
        #widgets = {
        #    'datebegin': DatePickerInput(format='%d.%m.%Y'), # default date-format %m/%d/%Y will be used
        #    'dateend': DatePickerInput(format='%d.%m.%Y'), # specify date-frmat
        #}