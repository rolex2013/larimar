from django import forms

from .models import YList, YListItem

class YListForm(forms.ModelForm):
    fields_disabled = ('fieldslist', 'company', 'datecreate', 'dateupdate', 'dateclose', 'author', 'authorupdate')

    class Meta:
        model = YList
        fields = ['name', 'description', 'members', 'is_active']
        #labels = {'Files':'Выберите файлы'}
        # widgets = {
        #     'datebegin': DatePickerInput(options={'format': 'DD.MM.YY'}),
        #     'dateend': DatePickerInput(options={'format': 'DD.MM.YY'})
        # }