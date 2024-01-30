# import requests
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from main.utils_model import TranslateFieldMixin, Dict_Model


# request, пробрасываемый сюда из main\request_exposer.py
exposed_request = ""


class Meta_Param(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=64)
    name_en = models.CharField(
        _("Наименование_en"), max_length=64, blank=True, null=True
    )
    datecreate = models.DateTimeField(_("Дата"), auto_now_add=True)
    # *** если is_service==True, то доступна регистрация Организаций пользователями и тестирование Системы в мультипользовательском режиме ***
    is_service = models.BooleanField(_("Система, как сервис"), default=True)
    is_active = models.BooleanField(_("Активность Системы"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    class Meta:
        ordering = ("datecreate",)

    def __str__(self):
        return self.datecreate.strftime("%d.%m.%Y %H:%M:%S") + "|" + self.name


class Meta_ObjectType(Dict_Model):
    shortname = models.CharField(_("Код"), max_length=16)
    tablename = models.CharField(_("Таблица"), max_length=64)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        verbose_name = _("Список типов объектов")
        verbose_name_plural = _("Списки типов объектов")


class Dict_ProtocolType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        verbose_name = _("Протокол оповещения")
        verbose_name_plural = _("Протоколы оповещений")


class Component(TranslateFieldMixin, MPTTModel):
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="component_children",
        verbose_name=_("Головной компонент"),
    )
    name_ru = models.CharField(
        _("Наименование_ru"), max_length=64, blank=True, null=True
    )
    name_en = models.CharField(
        _("Наименование_en"), max_length=64, blank=True, null=True
    )
    code = models.CharField(_("Код"), max_length=64)
    description_ru = models.CharField(
        _("Описание_ru"), max_length=256, blank=True, null=True
    )
    description_en = models.CharField(
        _("Описание_en"), max_length=256, blank=True, null=True
    )
    menu_ru = models.CharField(
        _("Пункт меню_ru"), max_length=256, blank=True, null=True
    )
    menu_en = models.CharField(
        _("Пункт меню_en"), max_length=256, blank=True, null=True
    )
    is_employee_default = models.BooleanField(
        _("Подключать сотруднику по-умолчанию"), default=False
    )
    is_client_default = models.BooleanField(
        _("Подключать клиенту по-умолчанию"), default=False
    )
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def menu(self):
        return self.trans_field(exposed_request, "menu")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ["code"]

    class Meta:
        verbose_name = _("Компонент")
        verbose_name_plural = _("Компоненты")


class Notification(TranslateFieldMixin, models.Model):
    objecttype = models.ForeignKey(
        "Meta_ObjectType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="meta_objecttype",
        verbose_name=_("Тип Объекта"),
    )
    objectid = models.PositiveIntegerField(_("ID объекта"), default=0)
    datecreate = models.DateTimeField(_("Дата"), auto_now_add=True)
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name=_("Автор")
    )
    type = models.ForeignKey(
        "Dict_ProtocolType",
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="protocol_type",
        verbose_name=_("Тип"),
    )
    sendfrom = models.CharField(_("От кого"), max_length=64, blank=True, null=True)
    theme = models.CharField(_("Тема"), max_length=256, blank=True, null=True)
    text = RichTextUploadingField(_("Текст"), max_length=1024)
    recipient = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="notify_recipient",
        verbose_name=_("Получатель"),
    )
    sendto = models.CharField(_("Кому"), max_length=64, blank=True, null=True)
    datesent = models.DateTimeField(
        _("Момент отправки"), auto_now_add=False, blank=True, null=True
    )
    dateread = models.DateTimeField(
        _("Момент прочтения"), auto_now_add=False, blank=True, null=True
    )
    response = models.CharField(_("Ответ"), max_length=128, blank=True, null=True)
    is_sent = models.BooleanField(_("Отправлено"), default=False)
    is_read_isauthor = models.BooleanField(_("Прочитано исходящее"), default=False)
    is_read_isrecipient = models.BooleanField(_("Прочитано входящее"), default=False)
    is_active = models.BooleanField(_("Активность"), default=True)

    def __str__(self):
        return (
            self.datecreate.strftime("%d.%m.%Y %H:%M:%S")
            + " | "
            + self.theme
            + " | "
            + self.author.username
        )

    class Meta:
        verbose_name = _("Оповещение")
        verbose_name_plural = _("Оповещения")


class ModelLog(TranslateFieldMixin, models.Model):
    componentname = models.CharField(_("Компонент"), max_length=16)
    modelname = models.CharField(_("Модель"), max_length=64)
    modelobjectid = models.IntegerField(_("Объект"))
    date = models.DateTimeField(_("Дата"), auto_now_add=True)
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name=_("Автор")
    )
    log = models.TextField()
    is_active = models.BooleanField(_("Активность"), default=True)

    def __str__(self):
        return (
            self.componentname
            + ". "
            + self.modelname
            + self.date.strftime("%d.%m.%Y, %H:%M")
            + " ("
            + self.author.username
            + ")"
            + self.log
        )

    class Meta:
        ordering = ("componentname", "modelname", "modelobjectid", "date")
        verbose_name = _("История Объекта")
        verbose_name_plural = _("Истории Объектов")


class Menu(TranslateFieldMixin, models.Model):
    name_ru = models.CharField(_("Наименование_ru"), max_length=128)
    name_en = models.CharField(
        _("Наименование_en"), max_length=128, blank=True, null=True
    )
    slug = models.CharField("slug", max_length=64)
    base_url = models.CharField(_("Основной URL"), max_length=128)
    description_ru = models.TextField(_("Описание_ru"), blank=True, null=True)
    description_en = models.TextField(_("Описание_en"), blank=True, null=True)
    # sort = models.PositiveSmallIntegerField(default=5, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Список меню")
        verbose_name_plural = _("Списки меню")


class MenuItem(TranslateFieldMixin, MPTTModel):
    title_ru = models.CharField(_("Наименование_ru"), default="title", max_length=128)
    title_en = models.CharField(_("Наименование_en"), default="title", max_length=128)
    menu = models.ForeignKey(
        "Menu",
        on_delete=models.CASCADE,
        related_name="menuitem_menu",
        verbose_name=_("Меню"),
    )
    component = models.ForeignKey(
        "Component",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="menuitem_component",
        verbose_name=_("Компонент"),
    )
    description_ru = models.TextField(_("Описание_ru"), null=True, blank=True)
    description_en = models.TextField(_("Описание_en"), null=True, blank=True)
    link_url = models.CharField("URL", max_length=128)
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="menuitem_children",
        verbose_name=_("Головной пункт меню"),
    )
    sort = models.PositiveSmallIntegerField(default=15, blank=True, null=True)
    is_active = models.BooleanField(_("Активность"), default=True)

    @property
    def title(self):
        return self.trans_field(exposed_request, "title")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    def __str__(self):
        return self.menu.name + " " + self.title

    class MPTTMeta:
        order_insertion_by = ["sort"]

    class Meta:
        verbose_name = _("Пункты меню")
        verbose_name_plural = _("Пункты меню")


# class Dict_Theme(TranslateFieldMixin, MPTTModel):
class Dict_Theme(Dict_Model, MPTTModel):
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="theme_children",
        verbose_name=_("Головная тематика"),
    )

    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class MPTTMeta:
        order_insertion_by = ["name_ru"]

    class Meta:
        verbose_name = _("Тематика")
        verbose_name_plural = _("Тематика")
