from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Company, Project, Task, TaskComment
from .models import ProjectStatusLog, TaskStatusLog
from .models import Dict_ProjectStatus, Dict_TaskStatus
from main.models import Notification
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


class ProjectForm(forms.ModelForm):
    #datebegin = forms.DateField(widget=AdminDateWidget())
    #datebegin = forms.DateField(widget=AdminSplitDateTime())

    disabled_fields = ('dateclose', 'author',)

    def clean(self):
        if self.cleaned_data['dateend'] < self.cleaned_data['datebegin']:
           self.cleaned_data['dateend'] = self.cleaned_data['datebegin']
        if self.action == 'update': 
           if self.cleaned_data['status'].id != self.initial['status']:
              # если вызов пришёл из ProjectUpdate и статус проекта был изменён, то пишем лог изменения 
              dict_status = Dict_ProjectStatus.objects.get(pk=self.cleaned_data['status'].id)
              ProjectStatusLog.objects.create(project_id=self.initial['id'], 
                                              status_id=dict_status.id, 
                                              author_id=self.user.id)
              if self.cleaned_data['status'].is_close: # == "Выполнен":
                 if self.user.id != self.initial['author']: 
                    # если проект закрывается Исполнителем, то уведомление отсылается Автору
                    self.cleaned_data['dateclose'] = datetime.datetime.today()
                    self.cleaned_data['percentage'] = 100  
                    #user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)    
                    user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)                                       
                    #send_mail('LarimarITGroup. Ваш Проект закрыт.', 'Уведомляем о закрытии Вашего Проекта!', settings.EMAIL_HOST_USER, [user_profile.email])
                    Notification.objects.create(type=user_profile.protocoltype,
                                                sendfrom=settings.EMAIL_HOST_USER,
                                                theme='Ваш Проект переведён в статус "'+dict_status.name+'"',
                                                text='Уведомляем об изменении статуса Вашего Проекта "'+self.cleaned_data['name']+'".',
                                                recipient_id=self.initial['author'],                                             
                                                sendto=user_profile.email,
                                                author_id=self.user.id)
              else:
                 self.cleaned_data['dateclose'] = None
           elif self.cleaned_data['assigner'].id != self.initial['assigner']:
              user_profile = UserProfile.objects.get(user=self.cleaned_data['assigner'].id, is_active=True)
              #send_mail('LarimarITGroup. Вы назначены исполнителем Проекта.', 'Уведомляем о назначении Вам Проекта!', settings.EMAIL_HOST_USER, [user_profile.email])
              Notification.objects.create(type=user_profile.protocoltype,
                                          sendfrom=settings.EMAIL_HOST_USER,
                                          theme='Вы назначены исполнителем Проекта.',
                                          text='Уведомляем о назначении Вам Проекта "'+self.cleaned_data['name']+'".',
                                          recipient_id=self.initial['assigner'],                                          
                                          sendto=user_profile.email,
                                          author_id=self.user.id)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму 

        if self.action == 'create':
           self.company = kwargs.pop('companyid') 
           super(ProjectForm, self).__init__(*args, **kwargs)
           companyid = self.company
        else:
           super(ProjectForm, self).__init__(*args, **kwargs)
           companyid = self.instance.company_id

        # в выпадающие списки для выбора Исполнителя (Руководителя) и участников проекта подбираем только тех юзеров, которые привязаны к этой организации (в админке)
        uc = UserCompanyComponentGroup.objects.filter(company_id=companyid).values_list('user_id', flat=True)
        usr = User.objects.filter(id__in=uc, is_active=True)
        self.fields['assigner'].queryset = usr
        self.fields['members'].queryset = usr

        # Исполнитель не может менять Исполнителя
        if self.user.id == self.initial['assigner']:
           self.fields['assigner'].disabled = True

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Project
        fields = ['name', 'description', 'members', 'assigner', 'cost', 'datebegin', 'dateend', 'structure_type', 'type', 'status', 'percentage', 'dateclose', 'is_active', 'id', 'author']
        widgets = {
            'datebegin': DatePickerInput(format='%d.%m.%Y'), # default date-format %m/%d/%Y will be used
            'dateend': DatePickerInput(format='%d.%m.%Y'), # specify date-frmat
        }

class TaskForm(forms.ModelForm):

    disabled_fields = ('dateclose', 'author',)

    def clean(self):
        if self.cleaned_data['dateend'] < self.cleaned_data['datebegin']:
           self.cleaned_data['dateend'] = self.cleaned_data['datebegin']
        # здесь надо поставить проверку на view.TaskUpdate
        if self.action == 'update':
           if self.cleaned_data['status'].id != self.initial['status']:
              # если вызов пришёл из TaskUpdate и статус задачи был изменён, то пишем лог изменения 
              dict_status = Dict_TaskStatus.objects.get(pk=self.cleaned_data['status'].id)
              TaskStatusLog.objects.create(task_id=self.initial['id'], 
                                           status_id=dict_status.id, 
                                           author_id=self.user.id)
              if self.cleaned_data['status'].is_close:
                 if self.user.id != self.initial['author']: 
                    self.cleaned_data['dateclose'] = datetime.datetime.today()
                    self.cleaned_data['percentage'] = 100              
                    #user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                    user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                    #send_mail('LarimarITGroup. Ваша Задача закрыта.', 'Уведомляем о закрытии Вашей Задачи!', settings.EMAIL_HOST_USER, [user_profile.email])                 
                    Notification.objects.create(type=user_profile.protocoltype,
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
              #send_mail('LarimarITGroup. Вы назначены исполнителем Задачи.', 'Уведомляем о назначении Вам Задачи!', settings.EMAIL_HOST_USER, [user_profile.email])
              Notification.objects.create(type=user_profile.protocoltype,
                                          sendfrom=settings.EMAIL_HOST_USER,
                                          theme='Вы назначены исполнителем Задачи.',
                                          text='Уведомляем о назначении Вам Задачи "'+self.cleaned_data['name']+'".',
                                          recipient_id=self.cleaned_data['assigner'],                                                
                                          sendto=user_profile.email,
                                          author_id=self.user.id)                                                     

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму
        if self.action == 'create':
           self.project = kwargs.pop('projectid') 
           super(TaskForm, self).__init__(*args, **kwargs)
           prj = Project.objects.get(id=self.project)
           companyid = prj.company_id
        else:
           super(TaskForm, self).__init__(*args, **kwargs)
           companyid = self.instance.project.company_id                

        # в выпадающий список для выбора Исполнителя подбираем только тех юзеров, которые привязаны к этой организации (в админке)
        uc = UserCompanyComponentGroup.objects.filter(company_id=companyid).values_list('user_id', flat=True)
        usr = User.objects.filter(id__in=uc, is_active=True)
        self.fields['assigner'].queryset = usr

        # Исполнитель не может менять Исполнителя
        if self.user.id == self.initial['assigner']:
           self.fields['assigner'].disabled = True

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigner', 'cost', 'datebegin', 'dateend', 'structure_type', 'type', 'status', 'percentage', 'dateclose', 'is_active', 'id', 'author']
        widgets = {
            'datebegin': DatePickerInput(format='%d.%m.%Y HH:mm'), # default date-format %m/%d/%Y will be used
            'dateend': DatePickerInput(format='%d.%m.%Y HH:mm'), # specify date-frmat
        }        

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['name', 'description', 'time', 'cost']


class FilterStatusForm(forms.ModelForm):                
    class Meta:
        model = Dict_ProjectStatus
        fields = ['name']