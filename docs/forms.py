from django.http import HttpResponse
# from ckeditor.widgets import CKEditorWidget
from django_ckeditor_5.widgets import CKEditor5Widget

from django import forms
from .models import Company, Doc, DocTask, DocTaskComment
from .models import Dict_DocStatus, Dict_DocType
from accounts.models import UserProfile
from companies.models import UserCompanyComponentGroup
from django.contrib.auth.models import User
from main.models import Notification, Meta_ObjectType
from main.utils import MultipleFileField

# from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
from django.contrib.auth.context_processors import auth
import datetime
from django.conf import settings
from django.core.mail import send_mail

from django.utils.translation import gettext_lazy as _


class DocForm(forms.ModelForm):
    # files = forms.FileField(
    #     label=_("Файлы документа"),
    #     widget=forms.ClearableFileInput(attrs={"multiple": True}),
    #     required=False,
    # )
    files = MultipleFileField(
        label=_("Файлы документа"),
        required=False,
    )
    # is_public = forms.BooleanField(label='Отметьте, если хотите опубликовать эту версию Документа', required=False)
    is_public = forms.BooleanField(label=_("Опубликован"), required=False)

    disabled_fields = ("datepublic", "author")  # , 'is_public')
    # disabled_fields = ('datecreate', 'author',)

    def clean(self):
        if self.action == "update":
            if self.cleaned_data["is_public"] is True:
                self.cleaned_data["datepublic"] = datetime.datetime.today()
            else:
                self.cleaned_data["datepublic"] = None
            if self.cleaned_data["status"].id != self.initial["status"]:
                if self.cleaned_data["status"].is_public:
                    self.cleaned_data["datepublic"] = datetime.datetime.today()
                    self.cleaned_data["is_public"] = True
                    if self.user.id != self.initial["author"]:
                        """
                        Сообщение и Уведомление высылаются Автору Документа, если его завершил не он
                        """
                        # self.cleaned_data['percentage'] = 100
                        # self.cleaned_data['phone'] = '+7(999)999-9998'
                        # #user_profile = UserProfile.objects.get(user=self.user.id, is_active=True)
                        user_profile = UserProfile.objects.get(
                            user=self.initial["author"], is_active=True
                        )
                        objecttypeid = Meta_ObjectType.objects.get(shortname="doc").id
                        send_mail(
                            _("1YES! Ваш Документ опубликован."),
                            _("Уведомляем о публикации Вашего Документа!"),
                            settings.EMAIL_HOST_USER,
                            [user_profile.email],
                        )
                        Notification.objects.create(
                            type=user_profile.protocoltype,
                            objecttype_id=objecttypeid,
                            objectid=self.initial["id"],
                            sendfrom=settings.EMAIL_HOST_USER,
                            theme=_("Ваш Документ опубликован!"),
                            text=_("Уведомляем об опубликовании Вашего Документа."),
                            recipient_id=self.initial["author"],
                            sendto=user_profile.email,
                            author_id=self.user.id,
                        )

                else:
                    self.cleaned_data["datepublic"] = None
                    self.cleaned_data["is_public"] = False
            elif self.cleaned_data["manager"].id != self.initial["manager"]:
                """
                Сообщение и Уведомление высылаются Менеджеру Документа, если не он сам себя назначил
                """
                user_profile = UserProfile.objects.get(
                    user=self.cleaned_data["manager"].id, is_active=True
                )
                objecttypeid = Meta_ObjectType.objects.get(shortname="doc").id
                send_mail(
                    _("1YES! Вы назначены менеджером Документа."),
                    _("Уведомляем о назначении Вам Документа!"),
                    settings.EMAIL_HOST_USER,
                    [user_profile.email],
                )
                Notification.objects.create(
                    type=user_profile.protocoltype,
                    objecttype_id=objecttypeid,
                    objectid=self.initial["id"],
                    sendfrom=settings.EMAIL_HOST_USER,
                    theme=_("Вы назначены менеджером Документа."),
                    text=_("Уведомляем о назначении Вам Документа")
                    + ' "'
                    + self.cleaned_data["name"]
                    + '".',
                    recipient_id=self.initial["manager"],
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
            # Менеджер не может менять Менеджера
            if self.user.id == self.initial["manager"]:
                self.fields["manager"].disabled = True
            dc = Doc.objects.filter(id=self.instance.id).first()
            if dc.doctask != 0:
                self.fields["is_public"].disabled = True

        # в выпадающие списки для выбора Менеджера и Участников Документа подбираем только тех юзеров, которые привязаны к этой организации (в админке)
        uc = UserCompanyComponentGroup.objects.filter(company_id=companyid).values_list(
            "user_id", flat=True
        )
        usr = User.objects.filter(id__in=uc, is_active=True)
        self.fields["manager"].queryset = usr
        self.fields["members"].queryset = usr
        self.fields["author"].initial = self.user.id

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = Doc
        fields = [
            "name",
            "description",
            "manager",
            "type",
            "status",
            "members",
            "datepublic",
            "is_active",
            "id",
            "author",
        ]
        # widgets = {
        #    'datebegin': DatePickerInput(format='%d.%m.%Y'), # default date-format %m/%d/%Y will be used
        #    'dateend': DatePickerInput(format='%d.%m.%Y'), # specify date-frmat
        # }


class DocTaskForm(forms.ModelForm):
    # files = forms.FileField(
    #     label=_("Файлы задачи"),
    #     widget=forms.ClearableFileInput(attrs={"multiple": True}),
    #     required=False,
    # )
    files = MultipleFileField(
        label=_("Файлы задачи"),
        required=False,
    )
    # comment = forms.CharField(label=_('Комментарий'), widget=forms.Textarea, required=False)
    # comment = forms.CharField(
    #     label=_("Комментарий"), widget=CKEditorWidget(), required=False
    # )
    comment = forms.CharField(
        label=_("Комментарий"),
        widget=CKEditor5Widget(
            attrs={"class": "django_ckeditor_5"}, config_name="extends"
        ),
        required=False,
    )
    disabled_fields = ("dateclose", "author")

    def clean(self):
        # if self.cleaned_data['dateend'] < self.cleaned_data['datebegin']:
        #    self.cleaned_data['dateend'] = self.cleaned_data['datebegin']
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
            "user", None
        )  # Выцепляем текущего юзера (To get request.user. Do not use kwargs.pop('user', None) due to potential security hole)
        self.action = kwargs.pop(
            "action", None
        )  # Узнаём, какая вьюха вызвала эту форму

        if self.action == "create":
            self.doc = kwargs.pop("docid")
            self.docver = kwargs.pop("docverid")
            super().__init__(*args, **kwargs)
            # doc = Doc.objects.get(id=self.doc)
            # docid = doc.id
            # print(self.docver)
        else:
            super().__init__(*args, **kwargs)
            self.doc = self.instance.doc_id
            self.docver = self.instance.docver_id
            # Исполнитель не может менять Исполнителя, если он не Автор
            if (
                self.user.id == self.initial["assigner"]
                and self.user.id != self.initial["author"]
            ):
                self.fields["assigner"].disabled = True

        # выцепляем id юзеров-участников Документа
        members_list = list(
            Doc.objects.filter(id=self.doc).values_list("members", flat=True)
        )
        # print(members_list)
        # в выпадающий список для выбора Исполнителя Задачи подбираем только тех юзеров, которые являются участниками этого Документа
        usr = User.objects.filter(id__in=members_list, is_active=True)
        # print (usr)
        self.fields["assigner"].queryset = usr
        self.fields["author"].initial = self.user.id
        for field in self.disabled_fields:
            self.fields[field].disabled = True

    class Meta:
        model = DocTask
        fields = [
            "description",
            "assigner",
            "dateend",
            "type",
            "status",
            "dateclose",
            "is_active",
            "id",
            "author",
        ]
        widgets = {
            "dateend": forms.DateTimeInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            # "comment": CKEditor5Widget(
            #     attrs={"class": "django_ckeditor_5"}, config_name="extends"
            # ),
        }


class DocTaskFormUpdate(DocTaskForm):
    comment = None


class DocTaskCommentForm(forms.ModelForm):
    # files = forms.FileField(
    #     label=_("Файлы комментария"),
    #     widget=forms.ClearableFileInput(attrs={"multiple": True}),
    #     required=False,
    # )
    files = MultipleFileField(
        label=_("Файлы комментария"),
        required=False,
    )

    class Meta:
        model = DocTaskComment
        # fields = ['name', 'description']
        fields = ["name", "description"]
