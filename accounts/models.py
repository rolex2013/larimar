from django.db import models
from django.urls import reverse, reverse_lazy
# from mptt.models import MPTTModel, TreeForeignKey
# from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field

from companies.models import Company

from django.utils.translation import gettext_lazy as _
# from main.utils_lang import TranslateFieldMixin

exposed_request = ""


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='result_user_profile', verbose_name=_("Пользователь"))
    company = models.ForeignKey('companies.Company', blank=True, null=True, on_delete=models.CASCADE, related_name='result_company_profile', verbose_name=_("Организация"))
    is_notify = models.BooleanField(_("Оповещать"), default=True)
    protocoltype = models.ForeignKey('main.Dict_ProtocolType', default=3, on_delete=models.CASCADE, related_name='result_protocol_type', verbose_name=_("Протокол оповещения"))
    lang = models.CharField(_("Язык"), max_length=5, blank=True, null=True)
    email = models.CharField("E-mail", max_length=64, blank=True, null=True)
    phone = models.CharField(_("Телефон"), max_length=16, blank=True, null=True)
    description = CKEditor5Field(
        _("Описание"), blank=True, null=True, config_name="extends"
    )

    is_active = models.BooleanField(_("Активность"), default=True)
    # is_del = models.BooleanField("Метка удаления", default=False)

    def get_absolute_url(self):
        return reverse('my_account:userprofile_detail', kwargs={'userid': self.user.pk, 'param': ' '})

    def __str__(self):
        # return (self.user.username + ' - ' + self.company.name)
        return (self.user.username)

    class Meta:
        # unique_together = ('user','company')
        # ordering = ('user')
        verbose_name = _('Профиль Пользователя')
        verbose_name_plural = _('Профили Пользователей')
