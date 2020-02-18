from django import forms
from .models import Project, Task, TaskComment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'assigner', 'datebegin', 'dateend']
        #name.widget.attrs.update({'class': 'form-control'})
    
    

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assigner', 'datebegin', 'dateend']

class TaskcommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['name', 'description']        