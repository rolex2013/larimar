from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Company, Project, Task, TaskComment, ProjectTaskStatusLog
from .models import Dict_ProjectStatus
#from django.contrib.admin.widgets import AdminDateWidget
#from django.contrib.admin.widgets import AdminSplitDateTime
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.context_processors import auth


class ProjectForm(forms.ModelForm):
    #datebegin = forms.DateField(widget=AdminDateWidget())
    #datebegin = forms.DateField(widget=AdminSplitDateTime())

    def clean(self):
        # здесь надо поставить проверку на view.ProjectUpdate
        if self.cleaned_data['status'].id != self.initial['status']:
           # если статус проекта был изменён, то пишем лог изменения 
           dict_status = Dict_ProjectStatus.objects.get(pk=self.cleaned_data['status'].id)
           ProjectTaskStatusLog.objects.create(logtype='P', 
                                               project_id=self.initial['id'], 
                                               status_id=dict_status.id, 
                                               author_id=self.user.id)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
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
        if self.cleaned_data['status'].id != self.initial['status']:
           # если статус задачи был изменён, то пишем лог изменения 
           dict_status = Dict_TaskStatus.objects.get(pk=self.cleaned_data['status'].id)
           ProjectTaskStatusLog.objects.create(logtype='T', 
                                               project_id=self.initial['id'], 
                                               status_id=dict_status.id, 
                                               author_id=self.user.id)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        super(ProjectForm, self).__init__(*args, **kwargs)

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
