from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Company, Content
from bootstrap_datepicker_plus import DatePickerInput


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'structure_type', 'type', 'is_active'] 
        #description = forms.CharField(widget=CKEditorWidget, label='')

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['name', 'description', 'company', 'type', 'datebegin', 'dateend', 'is_active']  
        widgets = {
            'datebegin': DatePickerInput(format='%d.%m.%Y HH:mm'),
            'dateend': DatePickerInput(format='%d.%m.%Y HH:mm'),
        }