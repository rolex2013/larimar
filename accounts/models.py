from django.db import models
from django.urls import reverse, reverse_lazy
#from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField

from companies.models import Company

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='result_user_profile', verbose_name="Пользователь")
    company = models.ForeignKey('companies.Company', blank=True, null=True, on_delete=models.CASCADE, related_name='result_company_profile', verbose_name="Организация")
    is_notify = models.BooleanField("Оповещать", default=True)
    protocoltype = models.ForeignKey('main.Dict_ProtocolType', blank=True, null=True, on_delete=models.CASCADE, related_name='result_protocol_type', verbose_name="Протокол оповещения")    
    email = models.CharField("E-mail", max_length=64, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=16, blank=True, null=True)
    description = RichTextUploadingField("Описание", blank=True, null=True)    
    is_active = models.BooleanField("Активность", default=True)

    def get_absolute_url(self):
        return reverse('my_account:userprofile_detail', kwargs={'userid': self.user.pk, 'param': ' '})  
    def __str__(self):
        #return (self.user.username + ' - ' + self.company.name)
        return (self.user.username)
    class Meta:
        #unique_together = ('user','company')
        #ordering = ('user')
        verbose_name = 'Профиль Пользователя'
        verbose_name_plural = 'Профили Пользователей'
