from django.db import models
from django.urls import reverse, reverse_lazy
from ckeditor_uploader.fields import RichTextUploadingField

from companies.models import Company

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='result_user_profile', verbose_name="Пользователь")
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='result_company_profile', verbose_name="Организация")
    description = RichTextUploadingField("Описание", blank=True, null=True)    
    is_active = models.BooleanField("Активность", default=True)

    def get_absolute_url(self):
        return reverse('my_account:userprofile_detail', kwargs={'userid': self.user.pk})  
    def __str__(self):
        return (self.user.username + ' - ' + self.company.name)
    class Meta:
        #unique_together = ('user','company')
        #ordering = ('user')
        verbose_name = 'Профиль Пользователя'
        verbose_name_plural = 'Профили Пользователей'
