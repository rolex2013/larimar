from django.db import models

from django.urls import reverse, reverse_lazy
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from ckeditor_uploader.fields import RichTextUploadingField


class Dict_CompanyStructureType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип в оргструктуре'
        verbose_name_plural = 'Типы в оргструктуре'
    def __str__(self):
        return (self.name)

class Dict_CompanyType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип организации'
        verbose_name_plural = 'Типы организаций'
    def __str__(self):
        return (self.name)

class Company(MPTTModel):    
    name = models.CharField("Наименование", max_length=64)
    #description = models.TextField("Описание")
    description = RichTextUploadingField("Описание")
    #company_up = models.ForeignKey('self', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='resultcompany_up', verbose_name="Головная организация")
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='company_children', verbose_name="Головная организация")
    structure_type = models.ForeignKey('Dict_CompanyStructureType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='company_structure_type', verbose_name="Тип в оргструктуре")
    type = models.ForeignKey('Dict_CompanyType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='company_type', verbose_name="Тип")
    datecreate = models.DateTimeField("Создана", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)    

    def get_absolute_url(self):
        #return reverse('my_project:company_detail', kwargs={'pk': self.pk})
        #return reverse('my_project:companies', kwargs={'pk': self.pk})
        return reverse('my_project:projects', kwargs={'companyid': self.pk, 'pk': '1'})          
               
    def __str__(self):
        return (self.name)
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'        

