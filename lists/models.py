from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import json

# from main.utils_lang import TranslateFieldMixin
from main.utils_model import Dict_Model

exposed_request = ""


class Dict_YListFieldType(Dict_Model):
    @property
    def name(self):
        return self.trans_field(exposed_request, "name")

    @property
    def description(self):
        return self.trans_field(exposed_request, "description")

    class Meta:
        verbose_name = _("Тип данных")
        verbose_name_plural = _("Типы данных")


class YList(models.Model):
    name = models.CharField(_("Наименование"), max_length=128)
    description = models.TextField(_("Описание"), blank=True, null=True)
    fieldslist = models.CharField(_("Список и тип полей"), max_length=1024)
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="ylistresultcompany",
        verbose_name=_("Компания"),
    )
    datecreate = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    dateupdate = models.DateTimeField(_("Дата изменения"), auto_now_add=True)
    dateclose = models.DateTimeField(_("Дата закрытия"), blank=True, null=True)
    authorupdate = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="ylist_author_update",
        verbose_name=_("Автор последних " "изменений"),
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="ylist_author",
        verbose_name=_("Автор"),
    )
    members = models.ManyToManyField(
        "auth.User", related_name="ylist_members", verbose_name=_("Участники")
    )
    is_active = models.BooleanField(_("Активность Списка"), default=True)

    @property
    def json_fieldslist(self):
        return [*json.loads(self.fieldslist)]

    @property
    def json_fieldsvalue(self):
        return json.loads(self.fieldslist).items()

    def add_column(self, key_name, key_value, position):
        d = json.loads(self.fieldslist)
        # if not d[key_name]:
        if key_name in d:
            # print('Столбец "Новый столбец" уже есть!')
            print(f"Столбец {key_name} уже есть!")
            return ""
        else:
            lst = list(d.items())
            lst.insert(position, (key_name, {"type": key_value}))
            d = dict(lst)
            self.fieldslist = json.dumps(d)
            self.save()
            return self.fieldslist

    def upd_column(self, key_name, key_value, position):
        d = json.loads(self.fieldslist)
        lst = list(d.items())
        key_name_old = lst[position][0]
        lst[position] = (key_name, {"type": key_value})
        # print("*** ", lst, key_name_old)
        d = dict(lst)
        self.fieldslist = json.dumps(d)
        self.save()
        # заменяем имя столбца в строках списка
        ylistitem = YListItem.objects.filter(ylist=self.id, is_active=True)
        # print("--- ", ylistitem)
        for yit in ylistitem:
            y = json.loads(yit.fieldslist)
            ylst = list(y.items())
            # print("&&& ", ylst)
            i = 0
            for yi_key, yi_val in ylst:
                # print("=== ", key_name_old, yi_key, i)
                if yi_key == key_name_old:
                    ylst[i] = (key_name, yi_val)
                    # print("/// ", ylst[i], i)
                    y = dict(ylst)
                    yit.fieldslist = json.dumps(y)
                    yit.save()
                    break
                i += 1

        return self.fieldslist

    def del_column(self, key_name):
        d = json.loads(self.fieldslist)
        d.pop(key_name, None)
        # d[key_name]["is_active"] = "False"  # вместо удаления меняем значение 'is_active'
        # всё-таки надо удалять!
        self.fieldslist = json.dumps(d)
        # print(type(d), d) #, type(lst), lst, self.fieldslist)
        self.save()
        return self.fieldslist

    def shift_column(self, col, prz):
        # сдвигаем столбцы влево или вправо
        shift = -1 if prz == 5 else 1
        d = json.loads(self.fieldslist)
        lst = list(d.items())
        # print("--- ", lst)
        lst[col], lst[col + shift] = lst[col + shift], lst[col]
        # print("+++ ", lst)
        d = dict(lst)
        self.fieldslist = json.dumps(d)
        self.save()
        return self.fieldslist

    def get_absolute_url(self):
        return reverse("my_list:ylist_items", kwargs={"pk": self.pk})

    def __str__(self):
        return (
            self.name
            + " "
            + self.datecreate.strftime("%d.%m.%Y %H:%M:%S")
            + " "
            + str(self.author)
        )

    class Meta:
        # ordering = ('sort',)
        verbose_name = _("Список")
        verbose_name_plural = _("Списки")


class YListItem(models.Model):
    fieldslist = models.TextField(_("Список и значения полей"), blank=True, null=True)
    ylist = models.ForeignKey(
        "YList",
        on_delete=models.CASCADE,
        related_name="ylistresult",
        verbose_name=_("Список"),
    )
    sort = models.PositiveSmallIntegerField(default=3, blank=True, null=True)
    datecreate = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    dateupdate = models.DateTimeField(_("Дата изменения"), auto_now_add=True)
    dateclose = models.DateTimeField(_("Дата закрытия"), blank=True, null=True)
    authorupdate = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="ylistitem_author_update",
        verbose_name=_("Автор последних " "изменений"),
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="ylistitem_author",
        verbose_name=_("Автор"),
    )
    is_active = models.BooleanField(_("Активность элемента Списка"), default=True)

    @property
    def json_fieldsname(self):
        return [*json.loads(self.fieldslist)]

    @property
    def json_fieldsvalue(self):
        return json.loads(self.fieldslist).items()

    def __str__(self):
        # return (self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + '|' + self.name)
        return self.fieldslist  # + "|" + str(self.ylist.id)

    def last_row(self):
        return (
            YListItem.objects.filter(ylist=self.ylist, is_active=True)
            .order_by("-sort")
            .first()
        )

    class Meta:
        ordering = ("sort",)
        verbose_name = _("Запись списка")
        verbose_name_plural = _("Записи списков")
