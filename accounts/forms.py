from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from companies.models import Company
from mptt.forms import MoveNodeForm, TreeNodeChoiceField

from django.utils.translation import ugettext_lazy as _

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
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    #def clean(self):
    #    usr = form.save()
    #    UserProfile.objects.create(user_id=usr.id) 
    #    return super(CompanyCreate, self).form_valid(form)  

class UserEnviteForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторно', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
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
           