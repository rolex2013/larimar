from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Company, Project, Task, TaskComment
#from django.contrib.admin.widgets import AdminDateWidget
from bootstrap_datepicker_plus import DatePickerInput


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'structure_type', 'type', 'is_active'] 
        #description = forms.CharField(widget=CKEditorWidget, label='')

class ProjectForm(forms.ModelForm):
    #datebegin = forms.DateField(widget=AdminDateWidget())
    dateend = forms.DateField(
                    widget=DatePickerInput(
                            options={
                                "format": "dd/MM/YYYY",
                                "autoclose": True
                            }
                    )
                )
    class Meta:
        model = Project
        fields = ['name', 'description', 'assigner', 'datebegin', 'dateend', 'structure_type', 'type', 'status', 'is_active']
        #widgets = {
        #    'datebegin': AdminDateWidget(),
        #    'dateend': AdminDateWidget(),
        #}

        #name.widget.attrs.update({'class': 'form-control'})    

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assigner', 'datebegin', 'dateend', 'structure_type', 'type', 'status', 'is_active']

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['name', 'description']        
