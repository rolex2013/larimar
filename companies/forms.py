
from django import forms
from .models import Company, StaffList, Staff, Summary, Content
from companies.models import UserCompanyComponentGroup
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import DatePickerInput

from mptt.forms import MoveNodeForm, TreeNodeChoiceField, TreeNodeMultipleChoiceField


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'currency', 'structure_type', 'type', 'is_support', 'is_active']
        #description = forms.CharField(widget=CKEditorWidget, label='')

class StaffListForm(forms.ModelForm):
    class Meta:
        model = StaffList
        fields = ['name', 'description', 'currency', 'salary', 'type', 'numberemployees', 'is_vacancy', 'vacancy', 'is_active'] 
        #description = forms.CharField(widget=CKEditorWidget, label='')

class StaffForm(forms.ModelForm):

    disabled_fields = ('stafflist', 'author',)

    def clean(self):
        if self.cleaned_data['rate'] > 1:
           self.cleaned_data['rate'] = 1            
        elif self.cleaned_data['rate'] <= 0:
           self.cleaned_data['rate'] = 0.1

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму
        if self.action == 'create': 
           self.stafflistid = kwargs.pop('stafflistid') 
           super(StaffForm, self).__init__(*args, **kwargs)
           stafflistid = self.stafflistid
           self.fields['stafflist'].initial = self.stafflistid            
        else:
           disabled_fields = ('user',)
           super(StaffForm, self).__init__(*args, **kwargs)
           stafflistid = self.instance.stafflist_id 
        ## в выпадающий список для выбора Сотрудника подбираем только тех юзеров, которые привязаны к этой компании, но не назначены на должности
        # у Сотрудника может быть несколько Должностей
        st_list = StaffList.objects.get(id=stafflistid)
        uc = UserCompanyComponentGroup.objects.filter(company_id=st_list.company_id).values_list('user_id', flat=True)
        #ucs = Staff.objects.filter(stafflist_id=stafflistid).values_list('user_id', flat=True)
        usr = User.objects.filter(id__in=uc, is_active=True) 
        self.fields['user'].queryset = usr
        self.fields['author'].initial = self.user.id        

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Staff
        fields = ['stafflist', 'user', 'rate', 'datebegin', 'dateend', 'author', 'is_active'] 
        #description = forms.CharField(widget=CKEditorWidget, label='')        

class StaffUpdateForm(forms.ModelForm):

    disabled_fields = ('stafflist', 'user', 'author',)

    def clean(self):
        if self.cleaned_data['rate'] > 1:
           self.cleaned_data['rate'] = 1            
        elif self.cleaned_data['rate'] <= 0:
           self.cleaned_data['rate'] = 0.1

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        #self.action = kwargs.pop('action')  # Узнаём, какая вьюха вызвала эту форму
        super(StaffUpdateForm, self).__init__(*args, **kwargs)
        stafflistid = self.instance.stafflist_id 
        ## в выпадающий список для выбора Сотрудника подбираем только тех юзеров, которые привязаны к этой компании, но не назначены на должности
        # у Сотрудника может быть несколько Должностей
        st_list = StaffList.objects.get(id=stafflistid)
        uc = UserCompanyComponentGroup.objects.filter(company_id=st_list.company_id).values_list('user_id', flat=True)
        usr = User.objects.filter(id__in=uc, is_active=True) 
        self.fields['user'].queryset = usr
        #self.fields['author'].initial = self.user.id        

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Staff
        fields = ['stafflist', 'user', 'rate', 'datebegin', 'dateend', 'author', 'is_active'] 
        #description = forms.CharField(widget=CKEditorWidget, label='')        

class SummaryForm(forms.ModelForm):

    class Meta:
        model = Summary
        fields = ['theme', 'candidatefirstname', 'candidatemiddlename', 'candidatelastname', 'email', 'phone', 'description', 'is_active']

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
            'datebegin': DatePickerInput(options={'format': 'DD.MM.YY HH:MM'}),
            'dateend': DatePickerInput(options={'format': 'DD.MM.YY HH:MM'}),
        }