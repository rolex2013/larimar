from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Company, Project, Task, TaskComment
from .models import ProjectStatusLog, TaskStatusLog
from .models import Dict_ProjectStatus, Dict_TaskStatus
#from django.contrib.admin.widgets import AdminDateWidget
#from django.contrib.admin.widgets import AdminSplitDateTime
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.context_processors import auth


class ProjectForm(forms.ModelForm):
    #datebegin = forms.DateField(widget=AdminDateWidget())
    #datebegin = forms.DateField(widget=AdminSplitDateTime())

    def clean(self):
        if self.action == 'update' and self.cleaned_data['status'].id != self.initial['status']:
           # если вызов пришёл из ProjectUpdate и статус проекта был изменён, то пишем лог изменения 
           dict_status = Dict_ProjectStatus.objects.get(pk=self.cleaned_data['status'].id)
           ProjectStatusLog.objects.create(project_id=self.initial['id'], 
                                           status_id=dict_status.id, 
                                           author_id=self.user.id)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму
        super(ProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ['name', 'description', 'assigner', 'datebegin', 'dateend', 'structure_type', 'type', 'status', 'is_active', 'id']
        widgets = {
            'datebegin': DatePickerInput(format='%d.%m.%Y'), # default date-format %m/%d/%Y will be used
            'dateend': DatePickerInput(format='%d.%m.%Y'), # specify date-frmat
        }

class TaskForm(forms.ModelForm):

    def clean(self):
        # здесь надо поставить проверку на view.TaskUpdate
        if self.action == 'update' and self.cleaned_data['status'].id != self.initial['status']:
           # если вызов пришёл из TaskUpdate и статус задачи был изменён, то пишем лог изменения 
           dict_status = Dict_TaskStatus.objects.get(pk=self.cleaned_data['status'].id)
           TaskStatusLog.objects.create(task_id=self.initial['id'], 
                                        status_id=dict_status.id, 
                                        author_id=self.user.id)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму
        super(TaskForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigner', 'datebegin', 'dateend', 'structure_type', 'type', 'status', 'is_active', 'id']
        widgets = {
            'datebegin': DatePickerInput(format='%d.%m.%Y HH:mm'), # default date-format %m/%d/%Y will be used
            'dateend': DatePickerInput(format='%d.%m.%Y HH:mm'), # specify date-frmat
        }        

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['name', 'description']        
