# from django.http import HttpResponse
# from ckeditor.widgets import CKEditorWidget
# import requests
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Project, Task, TaskComment  # , ProjectFile  # , Company

# from .models import ProjectStatusLog, TaskStatusLog
# from .models import Dict_TaskStatus, Dict_ProjectStatus
from main.models import Notification, Meta_ObjectType
from accounts.models import UserProfile
from companies.models import UserCompanyComponentGroup
from django.contrib.auth.models import User

# from django.contrib.admin.widgets import AdminDateWidget
# from django.contrib.admin.widgets import AdminSplitDateTime

# from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
# from .widgets import Date_PickerInput, Time_PickerInput, DateTime_PickerInput
# from django.contrib.admin.widgets import AdminDateWidget

# from django.contrib.auth.context_processors import auth
import datetime
from django.conf import settings
from django.core.mail import send_mail


# Create custom widget in your forms.py file.
class DateInput(forms.DateInput):
    input_type = "date"


class ProjectForm(forms.ModelForm):
    files = forms.FileField(
        label=_("Файлы проекта"),
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )
    disabled_fields = (
        "dateclose",
        "author",
    )

    def clean(self):
        if self.cleaned_data["dateend"] < self.cleaned_data["datebegin"]:
            self.cleaned_data["dateend"] = self.cleaned_data["datebegin"]
        if self.action == "update":
            if self.cleaned_data["status"].id != self.initial["status"]:
                if self.cleaned_data["status"].is_close:  # == "Выполнен":
                    self.cleaned_data["dateclose"] = datetime.datetime.today()
                    self.cleaned_data["percentage"] = 100
                    if self.user.id != self.initial["author"]:
                        """
                        Сообщение и Уведомление высылаются Автору Задачи, если её завершил не он
                        """
                        # user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                        user_profile = UserProfile.objects.get(
                            user=self.initial["author"], is_active=True
                        )
                        objecttypeid = Meta_ObjectType.objects.get(shortname="prj").id
                        send_mail(
                            _("1YES! Ваш Проект закрыт."),
                            _("Уведомляем о закрытии Вашего Проекта!"),
                            settings.EMAIL_HOST_USER,
                            [user_profile.email],
                        )
                        # print('==================')
                        Notification.objects.create(
                            type=user_profile.protocoltype,
                            objecttype_id=objecttypeid,
                            objectid=self.initial["id"],
                            sendfrom=settings.EMAIL_HOST_USER,
                            theme=_("Ваш Проект закрыт!"),
                            text=_("Уведомляем о закрытии Вашего Проекта."),
                            recipient_id=self.initial["author"],
                            sendto=user_profile.email,
                            author_id=self.user.id,
                        )
                else:
                    self.cleaned_data["dateclose"] = None
            elif self.cleaned_data["assigner"].id != self.initial["assigner"]:
                user_profile = UserProfile.objects.get(
                    user=self.cleaned_data["assigner"].id, is_active=True
                )
                objecttypeid = Meta_ObjectType.objects.get(shortname="prj").id
                # send_mail('LarimarITGroup. Вы назначены исполнителем Проекта.', 'Уведомляем о назначении Вам Проекта!', settings.EMAIL_HOST_USER, [user_profile.email])
                # print(user_profile.protocoltype)
                # print(self.cleaned_data['assigner'].id)
                Notification.objects.create(
                    type=user_profile.protocoltype,
                    objecttype_id=objecttypeid,
                    objectid=self.initial["id"],
                    sendfrom=settings.EMAIL_HOST_USER,
                    theme=_("Вы назначены исполнителем Проекта."),
                    text=_("Уведомляем о назначении Вам Проекта")
                    + ' "'
                    + self.cleaned_data["name"]
                    + '".',
                    recipient_id=self.cleaned_data["assigner"].id,
                    sendto=user_profile.email,
                    author_id=self.user.id,
                )

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
            # Исполнитель не может менять Исполнителя, если он не Автор
            if (
                self.user.id == self.initial["assigner"]
                and self.initial["assigner"] != self.initial["author"]
            ):
                self.fields["assigner"].disabled = True

        # в выпадающие списки для выбора Исполнителя (Руководителя) и участников проекта подбираем только тех юзеров, которые привязаны к этой организации (в админке)
        uc = UserCompanyComponentGroup.objects.filter(company_id=companyid).values_list(
            "user_id", flat=True
        )
        usr = User.objects.filter(id__in=uc, is_active=True)
        self.fields["assigner"].queryset = usr
        self.fields["members"].queryset = usr
        self.fields["author"].initial = self.user.id

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "members",
            "assigner",
            "currency",
            "cost",
            "datebegin",
            "dateend",
            "structure_type",
            "type",
            "status",
            "percentage",
            "is_active",
            "dateclose",
            "id",
            "author",
        ]

        widgets = {
            # "datebegin": DateInput(),
            "datebegin": forms.DateTimeInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),            
            "dateend": forms.DateTimeInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }


class TaskForm(forms.ModelForm):
    files = forms.FileField(
        label=_("Файлы задачи"),
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )

    disabled_fields = (
        "dateclose",
        "author",
    )

    def clean(self):
        if self.cleaned_data["dateend"] < self.cleaned_data["datebegin"]:
            self.cleaned_data["dateend"] = self.cleaned_data["datebegin"]
        # здесь надо поставить проверку на view.TaskUpdate
        if self.action == "update":
            if self.cleaned_data["status"].id != self.initial["status"]:
                if self.cleaned_data["status"].is_close:
                    self.cleaned_data["dateclose"] = datetime.datetime.today()
                    self.cleaned_data["percentage"] = 100
                    if self.user.id != self.initial["author"]:
                        """
                        Сообщение и Уведомление высылаются Автору Задачи, если её завершил не он
                        """
                        # user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                        user_profile = UserProfile.objects.get(
                            user=self.initial["author"], is_active=True
                        )
                        objecttypeid = Meta_ObjectType.objects.get(shortname="tsk").id
                        send_mail(
                            _("1YES! Ваша Задача закрыта."),
                            _("Уведомляем о закрытии Вашей Задачи!"),
                            settings.EMAIL_HOST_USER,
                            [user_profile.email],
                        )
                        Notification.objects.create(
                            type=user_profile.protocoltype,
                            objecttype_id=objecttypeid,
                            objectid=self.initial["id"],
                            sendfrom=settings.EMAIL_HOST_USER,
                            theme=_("Ваша Задача закрыта."),
                            text=_("Уведомляем о закрытии Вашей Задачи!"),
                            recipient_id=self.initial["author"],
                            sendto=user_profile.email,
                            author_id=self.user.id,
                        )
                else:
                    self.cleaned_data["dateclose"] = None
            elif self.cleaned_data["assigner"].id != self.initial["assigner"]:
                user_profile = UserProfile.objects.get(
                    user=self.cleaned_data["assigner"].id, is_active=True
                )
                objecttypeid = Meta_ObjectType.objects.get(shortname="tsk").id
                send_mail(
                    _("1YES! Вы назначены исполнителем Задачи."),
                    _("Уведомляем о назначении Вам Задачи!"),
                    settings.EMAIL_HOST_USER,
                    [user_profile.email],
                )
                Notification.objects.create(
                    type=user_profile.protocoltype,
                    objecttype_id=objecttypeid,
                    objectid=self.initial["id"],
                    sendfrom=settings.EMAIL_HOST_USER,
                    theme=_("Вы назначены исполнителем Задачи."),
                    text=_("Уведомляем о назначении Вам Задачи")
                    + ' "'
                    + self.cleaned_data["name"]
                    + '".',
                    recipient_id=self.cleaned_data["assigner"],
                    sendto=user_profile.email,
                    author_id=self.user.id,
                )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop(
            "user"
        )  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop("action")  # Узнаём, какая вьюха вызвала эту форму
        if self.action == "create":
            self.project = kwargs.pop("projectid")
            super(TaskForm, self).__init__(*args, **kwargs)
            prj = Project.objects.get(id=self.project)
            companyid = prj.company_id
        else:
            super(TaskForm, self).__init__(*args, **kwargs)
            companyid = self.instance.project.company_id
            self.project = self.instance.project_id
            # Исполнитель не может менять Исполнителя, если он не Автор
            if (
                self.user.id == self.initial["assigner"]
                and self.initial["assigner"] != self.initial["author"]
            ):
                self.fields["assigner"].disabled = True

        # в выпадающий список для выбора Исполнителя подбираем только тех юзеров, которые привязаны к этой организации (в админке)
        # uc = UserCompanyComponentGroup.objects.filter(company_id=companyid).values_list('user_id', flat=True)
        # usr = User.objects.filter(id__in=uc, is_active=True)
        # в выпадающий список для выбора Исполнителя Задачи подбираем только тех юзеров, которые являются участниками этого Проекта
        # выцепляем id юзеров-участников Проекта
        members_list = list(
            Project.objects.filter(id=self.project).values_list("members", flat=True)
        )
        usr = User.objects.filter(id__in=members_list, is_active=True)
        self.fields["assigner"].queryset = usr
        self.fields["author"].initial = self.user.id

        for field in self.disabled_fields:
            self.fields[field].disabled = True

        # self.fields["assigner"].empty_label = _("Пока не выбран")
        # self.fields["type"].empty_label = _("Пока не выбран")
        # self.fields["structure_type"].empty_label = _("Пока не выбран")
        # self.fields["status"].empty_label = _("Пока не выбран")

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "assigner",
            "cost",
            "datebegin",
            "dateend",
            "structure_type",
            "type",
            "status",
            "percentage",
            "is_active",
            "dateclose",
            "id",
            "author",
        ]
        widgets = {
            "datebegin": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "dateend": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }


class TaskCommentForm(forms.ModelForm):
    files = forms.FileField(
        label=_("Файлы комментария"),
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )

    class Meta:
        model = TaskComment
        fields = ["name", "description", "time", "cost"]


# class FilterStatusForm(forms.ModelForm):
#     class Meta:
#         model = Dict_ProjectStatus
#         fields = ["name"]
