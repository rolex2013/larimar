from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from companies.models import Company

class UserRegistrationForm(forms.ModelForm):
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

    #def clean(self):
    #    usr = form.save()
    #    UserProfile.objects.create(user_id=usr.id) 
    #    return super(CompanyCreate, self).form_valid(form)  

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        #self.user = kwargs.pop('user')
        self.request = kwargs.pop('request')
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(id=self.request.session['_auth_user_companies_id'][0])
    class Meta:
        model = UserProfile
        fields = ['company', 'description']        