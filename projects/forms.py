from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Company, Project, Task, TaskComment, ProjectFile
#from .models import ProjectStatusLog, TaskStatusLog
from .models import Dict_ProjectStatus, Dict_TaskStatus
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


class ProjectForm(forms.ModelForm):
    #datebegin = forms.DateField(widget=AdminDateWidget())
    #datebegin = forms.DateField(widget=AdminSplitDateTime())

    files = forms.FileField(label='Файлы проекта', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    disabled_fields = ('dateclose', 'author',)

    def clean(self):
        if self.cleaned_data['dateend'] < self.cleaned_data['datebegin']:
           self.cleaned_data['dateend'] = self.cleaned_data['datebegin']
        if self.action == 'update': 
           if self.cleaned_data['status'].id != self.initial['status']:
              # если вызов пришёл из ProjectUpdate и статус проекта был изменён, то пишем лог изменения (это переехало в переопределение метода save в модели)
              #dict_status = Dict_ProjectStatus.objects.get(pk=self.cleaned_data['status'].id)
              #ProjectStatusLog.objects.create(project_id=self.initial['id'], 
              #                                status_id=dict_status.id, 
              #                                author_id=self.user.id)
              if self.cleaned_data['status'].is_close: # == "Выполнен":
                 if self.user.id != self.initial['author']: 
                    # если проект закрывается Исполнителем, то уведомление отсылается Автору
                    self.cleaned_data['dateclose'] = datetime.datetime.today()
                    self.cleaned_data['percentage'] = 100  
                    #user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)    
                    user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                    objecttypeid = Meta_ObjectType.objects.get(shortname='prj').id                                       
                    send_mail('1YES. Ваш Проект закрыт.', 'Уведомляем о закрытии Вашего Проекта!', settings.EMAIL_HOST_USER, [user_profile.email])
                    #print('==================')
                    Notification.objects.create(type=user_profile.protocoltype,
                                                objecttype_id=objecttypeid,
                                                objectid=self.initial['id'],
                                                sendfrom=settings.EMAIL_HOST_USER,
                                                theme='Ваш Проект закрыт!',
                                                text='Уведомляем о закрытии Вашего Проекта.',
                                                recipient_id=self.initial['author'],                                             
                                                sendto=user_profile.email,
                                                author_id=self.user.id)
              else:
                 self.cleaned_data['dateclose'] = None
           elif self.cleaned_data['assigner'].id != self.initial['assigner']:
              user_profile = UserProfile.objects.get(user=self.cleaned_data['assigner'].id, is_active=True)
              objecttypeid = Meta_ObjectType.objects.get(shortname='prj').id
              #send_mail('LarimarITGroup. Вы назначены исполнителем Проекта.', 'Уведомляем о назначении Вам Проекта!', settings.EMAIL_HOST_USER, [user_profile.email])
              #print(user_profile.protocoltype)
              #print(self.cleaned_data['assigner'].id)
              Notification.objects.create(type=user_profile.protocoltype,
                                          objecttype_id=objecttypeid,  
                                          objectid=self.initial['id'],            
                                          sendfrom=settings.EMAIL_HOST_USER,
                                          theme='Вы назначены исполнителем Проекта.',
                                          text='Уведомляем о назначении Вам Проекта "'+self.cleaned_data['name']+'".',
                                          recipient_id=self.cleaned_data['assigner'].id,                                          
                                          sendto=user_profile.email,
                                          author_id=self.user.id)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')      # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму 

        if self.action == 'create':
           self.company = kwargs.pop('companyid') 
           super().__init__(*args, **kwargs)
           companyid = self.company
        else:
           super().__init__(*args, **kwargs)
           companyid = self.instance.company_id
           # Исполнитель не может менять Исполнителя, если он не Автор
           if self.user.id == self.initial['assigner'] and self.initial['assigner'] != self.initial['author']:
              self.fields['assigner'].disabled = True           

        # в выпадающие списки для выбора Исполнителя (Руководителя) и участников проекта подбираем только тех юзеров, которые привязаны к этой организации (в админке)
        uc = UserCompanyComponentGroup.objects.filter(company_id=companyid).values_list('user_id', flat=True)
        usr = User.objects.filter(id__in=uc, is_active=True)
        self.fields['assigner'].queryset = usr
        self.fields['members'].queryset = usr
        self.fields['author'].initial = self.user.id

        for field in self.disabled_fields:
            self.fields[field].disabled = True       

    class Meta:
        model = Project
        fields = ['name', 'description', 'members', 'assigner', 'currency', 'cost', 'datebegin', 'dateend', 'structure_type', 'type', 'status', 'percentage', 'is_active', 'dateclose', 'id', 'author']
        #labels = {'Files':'Выберите файлы'}
        widgets = {
            'datebegin': DatePickerInput(format='%d.%m.%Y'), # default date-format %m/%d/%Y will be used
            'dateend': DatePickerInput(format='%d.%m.%Y') # specify date-frmat,
            #'docfile': forms.ClearableFileInput(attrs={'multiple': True}),
            #'files': forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
        }

class TaskForm(forms.ModelForm):

    files = forms.FileField(label='Файлы задачи', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    disabled_fields = ('dateclose', 'author',)

    def clean(self):
        if self.cleaned_data['dateend'] < self.cleaned_data['datebegin']:
           self.cleaned_data['dateend'] = self.cleaned_data['datebegin']
        # здесь надо поставить проверку на view.TaskUpdate
        if self.action == 'update':
           if self.cleaned_data['status'].id != self.initial['status']:
              # если вызов пришёл из TaskUpdate и статус задачи был изменён, то пишем лог изменения (это переехало в переопределение метода save в модели) 
              #dict_status = Dict_TaskStatus.objects.get(pk=self.cleaned_data['status'].id)
              #TaskStatusLog.objects.create(task_id=self.initial['id'], 
              #                             status_id=dict_status.id, 
              #                             author_id=self.user.id)
              if self.cleaned_data['status'].is_close:
                 if self.user.id != self.initial['author']: 
                    self.cleaned_data['dateclose'] = datetime.datetime.today()
                    self.cleaned_data['percentage'] = 100              
                    #user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                    user_profile = UserProfile.objects.get(user=self.initial['author'], is_active=True)
                    objecttypeid = Meta_ObjectType.objects.get(shortname='tsk').id                    
                    send_mail('1Yes. Ваша Задача закрыта.', 'Уведомляем о закрытии Вашей Задачи!', settings.EMAIL_HOST_USER, [user_profile.email])                 
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
              send_mail('1Yes. Вы назначены исполнителем Задачи.', 'Уведомляем о назначении Вам Задачи!', settings.EMAIL_HOST_USER, [user_profile.email])
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
        if self.action == 'create':
           self.project = kwargs.pop('projectid') 
           super(TaskForm, self).__init__(*args, **kwargs)
           prj = Project.objects.get(id=self.project)
           companyid = prj.company_id         
        else:
           super(TaskForm, self).__init__(*args, **kwargs)
           companyid = self.instance.project.company_id
           self.project = self.instance.project_id      
           # Исполнитель не может менять Исполнителя, если он не Автор
           if self.user.id == self.initial['assigner'] and self.initial['assigner'] != self.initial['author']:
              self.fields['assigner'].disabled = True                         
 
        # в выпадающий список для выбора Исполнителя подбираем только тех юзеров, которые привязаны к этой организации (в админке)
        #uc = UserCompanyComponentGroup.objects.filter(company_id=companyid).values_list('user_id', flat=True)
        #usr = User.objects.filter(id__in=uc, is_active=True)
        # в выпадающий список для выбора Исполнителя Задачи подбираем только тех юзеров, которые являются участниками этого Проекта 
        # выцепляем id юзеров-участников Проекта
        members_list = list(Project.objects.filter(id=self.project).values_list('members', flat=True))         
        usr = User.objects.filter(id__in=members_list, is_active=True)          
        self.fields['assigner'].queryset = usr
        self.fields['author'].initial = self.user.id        

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigner', 'cost', 'datebegin', 'dateend', 'structure_type', 'type', 'status', 'percentage', 'is_active', 'dateclose', 'id', 'author']
        widgets = {
            'datebegin': DatePickerInput(format='%d.%m.%Y %H:%M'), # default date-format %m/%d/%Y will be used
            'dateend': DatePickerInput(format='%d.%m.%Y %H:%M'), # specify date-frmat
        }        

class TaskCommentForm(forms.ModelForm):

    files = forms.FileField(label='Файлы комментария', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = TaskComment
        fields = ['name', 'description', 'time', 'cost']


class FilterStatusForm(forms.ModelForm):                
    class Meta:
        model = Dict_ProjectStatus
        fields = ['name']

#
#class DateForm(forms.Form):
#    date = forms.DateTimeField(
#        input_formats=['%d/%m/%Y %H:%M'],
#        widget=forms.DateTimeInput(attrs={
#            'class': 'form-control datetimepicker-input',
#            'data-target': '#datetimepicker1'
#        })
#    )