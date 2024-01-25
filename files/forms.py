from django import forms

from .models import Dict_Theme, Dict_FolderType, Folder, FolderFile

# from main.models import Notification, Meta_ObjectType
from accounts.models import UserProfile
from companies.models import UserCompanyComponentGroup
from django.contrib.auth.models import User

# from django.contrib.admin.widgets import AdminDateWidget
# from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.auth.context_processors import auth
import datetime
from django.conf import settings

# from django.core.mail import send_mail

from django.utils.translation import gettext_lazy as _


class FolderForm(forms.ModelForm):
    files = forms.FileField(
        label=_("Файлы папки"),
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )

    disabled_fields = ("author",)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop(
            "user"
        )  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop("action")  # Узнаём, какая вьюха вызвала эту форму

        if self.action == "create":
            self.company = kwargs.pop("companyid")
            super().__init__(*args, **kwargs)
            companyid = self.company
        else:
            super().__init__(*args, **kwargs)
            companyid = self.instance.company_id

        self.fields["author"].initial = self.user.id

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Folder
        fields = ["name", "description", "theme", "type", "is_active", "id", "author"]
        # labels = {'Files':'Выберите файлы'}


class UploadFilesForm(forms.Form):
    files = forms.FileField(
        label=_("Файлы папки"),
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )
