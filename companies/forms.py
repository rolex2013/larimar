from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Company, Content
from bootstrap_datepicker_plus import DatePickerInput

from mptt.forms import MoveNodeForm, TreeNodeChoiceField, TreeNodeMultipleChoiceField


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'structure_type', 'type', 'is_active'] 
        #description = forms.CharField(widget=CKEditorWidget, label='')

class ContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.companies = kwargs.pop('org')
        super(ContentForm, self).__init__(*args, **kwargs)
        #self.fields['company'].queryset = Company.objects.filter(id__in=self.companies) # это без иерархии
        #self.fields['company'] = TreeNodeChoiceField(queryset=Company.objects.all(), level_indicator = u'---') # из документации
        self.fields['company'] = TreeNodeMultipleChoiceField(queryset=Company.objects.filter(id__in=self.companies), level_indicator = u'---') # с иерархией    
    class Meta:
        model = Content
        fields = ['name', 'announcement', 'description', 'is_ontop', 'company', 'type', 'datebegin', 'dateend', 'place']  
        widgets = {
            'datebegin': DatePickerInput(format='%d.%m.%Y HH:mm'),
            'dateend': DatePickerInput(format='%d.%m.%Y HH:mm'),
        }