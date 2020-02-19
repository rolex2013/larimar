from django.http import HttpResponse
from django import forms
from .models import Company, Project, Task, TaskComment

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'type', 'is_active'] 

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'assigner', 'datebegin', 'dateend', 'type', 'status', 'is_active']
        #name.widget.attrs.update({'class': 'form-control'})    

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assigner', 'datebegin', 'dateend', 'type', 'status', 'is_active']

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['name', 'description']        
