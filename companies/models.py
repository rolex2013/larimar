from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field

from django.urls import reverse, reverse_lazy
from django.utils import timezone

# import datetime

from mptt.models import MPTTModel, TreeForeignKey

# from main.models import Component

# from django.db.models.query import QuerySet
# from django_group_by import GroupByMixin

from django.utils.translation import gettext_lazy as _

# from main.utils_lang import TranslateFieldMixin
from main.utils_model import Dict_Model


exposed_request = ""


class Dict_CompanyStructureType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta(Dict_Model.Meta):
        verbose_name = _("Тип в оргструктуре")
        verbose_name_plural = _("Типы в оргструктуре")


class Dict_CompanyType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta(Dict_Model.Meta):
        verbose_name = _("Тип организации")
        verbose_name_plural = _("Типы организаций")


class Dict_PositionType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta(Dict_Model.Meta):
        verbose_name = _("Тип должности")
        verbose_name_plural = _("Типы должностей")


class Dict_ContentType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta(Dict_Model.Meta):
        verbose_name = _("Тип контента")
        verbose_name_plural = _("Типы контента")


class Dict_ContentPlace(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta(Dict_Model.Meta):
        verbose_name = _("Место отображения контента")
        verbose_name_plural = _("Места отображения контента")


class Company(MPTTModel):
    name = models.CharField(_("Наименование"), max_length=64)
    # description = models.TextField("Описание")
    description = RichTextUploadingField(_("Описание"))
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="company_children",
        verbose_name=_("Головная организация"),
    )
    currency = models.ForeignKey(
        "finance.Dict_Currency",
        on_delete=models.CASCADE,
        related_name="company_currency",
        verbose_name=_("Валюта"),
    )
    structure_type = models.ForeignKey(
        "Dict_CompanyStructureType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="company_structure_type",
        verbose_name=_("Тип в оргструктуре"),
    )
    type = models.ForeignKey(
        "Dict_CompanyType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="company_type",
        verbose_name=_("Тип"),
    )
    is_support = models.BooleanField(_("Служба техподдержки"), default=False)
    # groups = models.ManyToManyField('auth.Group', related_name='company_groups', verbose_name="Группы")
    datecreate = models.DateTimeField(_("Создана"), auto_now_add=True)
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name=_("Автор")
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    def get_absolute_url(self):
        # return reverse('my_project:projects', kwargs={'companyid': self.pk, 'pk': '1'})
        return reverse("my_company:stafflist", kwargs={"companyid": self.pk, "pk": "1"})

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["tree_id", "level"]
        verbose_name = _("Организация")
        verbose_name_plural = _("Организации")


# class UserCompany(models.Model):
#    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='result_user', verbose_name="Пользователь")
#    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='result_company', verbose_name="Организация")
#    is_active = models.BooleanField("Активность", default=True)
#
#    def __str__(self):
#        return (self.user.username + ' - ' + self.company.name)
#    class Meta:
#        unique_together = ('user', 'company')
#        ordering = ('user','company')
#        verbose_name = 'Пользователь Организации'
#        verbose_name_plural = 'Пользователи Организаций'


class UserCompanyComponentGroup(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="result_user",
        verbose_name=_("Пользователь"),
    )
    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="result_company",
        verbose_name=_("Организация"),
    )
    component = models.ForeignKey(
        "main.Component",
        on_delete=models.CASCADE,
        related_name="result_component",
        verbose_name=_("Компонент"),
    )
    group = models.ForeignKey(
        "auth.Group",
        on_delete=models.CASCADE,
        related_name="result_group",
        verbose_name=_("Группа"),
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    def __str__(self):
        return (
            self.user.username
            + " - "
            + self.company.name
            + " - "
            + self.component.name
            + " - "
            + self.group.name
        )

    class Meta:
        unique_together = ("user", "company", "component", "group")
        ordering = ("user", "company", "component", "group")
        verbose_name = _("Пользователь и Группа Организации и Компонента")
        verbose_name_plural = _("Пользователи и Группы Организаций и Компонентов")


# class ContentQuerySet(QuerySet, GroupByMixin):
#    pass


class StaffList(MPTTModel):
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="staff_children",
        verbose_name=_("Головная должность"),
    )
    company = models.ForeignKey(
        "Company",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="related_company",
        verbose_name=_("Организация"),
    )
    name = models.CharField(_("Наименование"), max_length=64)
    description = models.TextField(_("Описание"), null=True, blank=True)
    type = models.ForeignKey(
        "Dict_PositionType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="position_type",
        verbose_name=_("Тип должности"),
    )
    currency = models.ForeignKey(
        "finance.Dict_Currency",
        on_delete=models.CASCADE,
        related_name="related_currency",
        verbose_name=_("Валюта"),
    )
    salary = models.DecimalField(_("Оклад"), max_digits=14, decimal_places=2)
    numberemployees = models.PositiveIntegerField(_("Кол-во сотрудников"), default=1)
    vacancy = RichTextUploadingField(_("Описание вакансии"), null=True, blank=True)
    datecreate = models.DateTimeField(_("Создана"), auto_now_add=True)
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name=_("Автор")
    )
    is_vacancy = models.BooleanField(_("Вакансия"), default=False)
    is_active = models.BooleanField(_("Активность"), default=True)

    def get_absolute_url(self):
        return reverse("my_company:staffs", kwargs={"stafflistid": self.pk, "pk": "0"})

    def __str__(self):
        return self.company.name + ". " + self.name

    class MPTTMeta:
        order_insertion_by = ["company", "name"]

    class Meta:
        verbose_name = _("Штатное расписание")
        verbose_name_plural = _("Штатные расписания")


class Staff(models.Model):
    stafflist = models.ForeignKey(
        "StaffList",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="staff_stafflist",
        verbose_name=_("Должность"),
    )
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="staff_user",
        verbose_name=_("Пользователь"),
    )
    rate = models.DecimalField(
        _("Ставка (0,1 - 1)"), max_digits=3, decimal_places=2, default=1
    )
    datebegin = models.DateField(_("Начало работы"))
    dateend = models.DateField(_("Окончание работы"), null=True, blank=True)
    datecreate = models.DateTimeField(_("Создана"), auto_now_add=True)
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name=_("Автор")
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    def get_absolute_url(self):
        return reverse(
            "my_company:staffs", kwargs={"stafflistid": self.stafflist.id, "pk": "0"}
        )

    def __str__(self):
        return (
            self.stafflist.company.name
            + " - "
            + self.stafflist.name
            + " - "
            + self.user.username
        )

    class Meta:
        # unique_together = ('stafflist','user')
        ordering = ("stafflist", "user")
        verbose_name = _("Сотрудник")
        verbose_name_plural = _("Сотрудники")


class Summary(models.Model):
    stafflist = models.ForeignKey(
        "StaffList",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="summary_stafflist",
        verbose_name=_("Должность"),
    )
    theme = models.CharField(_("Тема"), max_length=1024)
    candidatefirstname = models.CharField(_("Имя"), max_length=64)
    candidatemiddlename = models.CharField(
        _("Отчество"), max_length=64, blank=True, null=True
    )
    candidatelastname = models.CharField(_("Фамилия"), max_length=64)
    email = models.CharField(_("E-mail"), max_length=64)
    phone = models.CharField(_("Телефон"), max_length=16)
    # description = RichTextUploadingField(_("Описание"), blank=True, null=True)
    description = CKEditor5Field(_("Описание"), blank=True, null=True, config_name="extends")
    datecreate = models.DateTimeField(_("Создано"), auto_now_add=True)
    # document = models.FileField(upload_to='documents/summary/')
    is_active = models.BooleanField(_("Активность"), default=True)

    def get_absolute_url(self):
        # return reverse('my_main:vacancy_detail', kwargs={'stafflistid': self.stafflist.id})
        return reverse("my_main:vacancies")

    def __str__(self):
        middlename = self.candidatemiddlename
        if self.candidatemiddlename is None:
            middlename = ""
        return (
            self.stafflist.company.name
            + " -- "
            + self.stafflist.name
            + " - "
            + self.candidatefirstname
            + " "
            + middlename
            + " "
            + self.candidatelastname
        )

    class Meta:
        # unique_together = ('stafflist','user')
        ordering = ("stafflist",)
        verbose_name = _("Резюме")
        verbose_name_plural = _("Резюме")


class Content(models.Model):
    # objects = ContentQuerySet.as_manager()
    name = models.CharField(_("Заголовок"), max_length=1024)
    # announcement = models.TextField(_("Анонс"), max_length=10240, blank=True, null=True)
    announcement = CKEditor5Field(
        _("Анонс"), max_length=10240, blank=True, config_name="extends"
    )
    # description = RichTextUploadingField(_("Текст"), blank=True, null=True)
    description = CKEditor5Field(
        _("Текст"), blank=True, config_name="extends"
    )
    datebegin = models.DateTimeField(_("Дата публикации"))
    dateend = models.DateTimeField(_("Дата снятия с публикации"))
    is_ontop = models.BooleanField(_("Всегда наверху"), default=False)
    type = models.ForeignKey(
        "Dict_ContentType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="content_type",
        verbose_name=_("Тип"),
    )
    # company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='content_company', verbose_name=_("Организация"))
    company = models.ManyToManyField(
        "Company", related_name="content_companies", verbose_name=_("Организации")
    )
    datecreate = models.DateTimeField(_("Создан"), auto_now_add=True)
    # dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name=_("Автор")
    )
    # is_public = models.BooleanField("Только для внешнего сайта", default=False)
    # is_forprofile = models.BooleanField("Только для профиля", default=False)
    # is_private = models.BooleanField("Приватно", default=False)
    place = models.ForeignKey(
        "Dict_ContentPlace",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="content_place",
        verbose_name=_("Место"),
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    def get_absolute_url(self):
        # return reverse('my_main:home')
        return reverse("my_company:content_detail", kwargs={"pk": self.pk})

    def __str__(self):
        # return (self.company.name + ' - ' + self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + ' - ' + self.type.name + ' - ' + self.name + ' - ' + self.author.username)
        return (
            self.datecreate.strftime("%d.%m.%Y %H:%M:%S")
            + " - "
            + self.type.name
            + " - "
            + self.name
            + " - "
            + self.author.username
        )

    class Meta:
        # ordering = ('company','type','datecreate')
        ordering = ("-is_ontop", "-id")
        verbose_name = _("Контент")
        verbose_name_plural = _("Контент")
