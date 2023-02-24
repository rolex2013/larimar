from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from companies.models import Company, UserCompanyComponentGroup
from mptt.forms import MoveNodeForm, TreeNodeChoiceField

from django.utils.translation import gettext_lazy as _

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Повторно'), widget=forms.PasswordInput)
    is_org_register = forms.BooleanField(label=_('Зарегистрировать свою Компанию?'), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']

    #def clean(self):
    #    usr = form.save()
    #    UserProfile.objects.create(user_id=usr.id) 
    #    return super(CompanyCreate, self).form_valid(form)
"""
class UserAddForm(forms.Select):
    #user = forms.ChoiceField(UserProfile.objects.filter('is_active=True'))
    #user = forms.ChoiceField(label="", initial='', widget=forms.Select({"vvfgfg","kkjkjkjkkjk"}), required=True)
    a = 1

    class Meta:
        model = User
        fields = ('username', 'is_staff')
"""
class UserSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['username'] = value.instance.username
        return option

class UserAddForm(forms.ModelForm):

    is_staff = forms.BooleanField(label='Отметьте, если это сотрудник, а не клиент', required=False)

    # Надо из выпадающего списка юзеров исключить уже привязанных к этой организации
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        companyid = self.instance.id
        #uc = UserCompanyComponentGroup.objects.filter(is_active=True).exclude(company_id=companyid, user__is_active=True).values_list('user_id', flat=True).distinct()
        #usr = User.objects.filter(id__in=uc, is_active=True)
        uc = UserCompanyComponentGroup.objects.filter(is_active=True, company_id=companyid, user__is_active=True).values_list('user', flat=True).distinct()
        usr = User.objects.filter(is_active=True).exclude(id__in=uc)
        self.fields['user'].queryset = usr
        #print(uc)
    class Meta:
        model = UserCompanyComponentGroup
        fields = ['user']
        widgets = {'user': UserSelect}

class UserEnviteForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторно', widget=forms.PasswordInput) 

    def __init__(self, *args, **kwargs):
        super(UserEnviteForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].help_text = '<br />(отметьте, если это сотрудник вашей Организации)'  

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'is_staff')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        #self.user = kwargs.pop('user')
        self.companies = kwargs.pop('org')
        #print(self.companies)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        #self.fields['company'].queryset = Company.objects.filter(id__in=self.companies) # это без иерархии
        #self.fields['company'] = TreeNodeChoiceField(queryset=Company.objects.all(), level_indicator = u'---') # из документации
        self.fields['company'] = TreeNodeChoiceField(queryset=Company.objects.filter(id__in=self.companies), level_indicator = u'---') # с иерархией
    class Meta:
        model = UserProfile
        fields = ['company', 'description', 'is_notify', 'protocoltype', 'email', 'phone']     
           