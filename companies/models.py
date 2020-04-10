from django.db import models

from django.urls import reverse, reverse_lazy
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from ckeditor_uploader.fields import RichTextUploadingField

#from main.models import Component

#from django.db.models.query import QuerySet
#from django_group_by import GroupByMixin


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
        return reverse('my_project:projects', kwargs={'companyid': self.pk, 'pk': '1'})          
               
    def __str__(self):
        return (self.name)
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'        

#class UserCompany(models.Model):
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
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='result_user', verbose_name="Пользователь")
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='result_company', verbose_name="Организация")
    component = models.ForeignKey('main.Component', on_delete=models.CASCADE, related_name='result_component', verbose_name="Компонент")        
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE, related_name='result_group', verbose_name="Группа")
    is_active = models.BooleanField("Активность", default=True)
    
    def __str__(self):
        return (self.user.username + ' - ' + self.company.name + ' - ' + self.component.name + ' - ' + self.group.name)
    class Meta:
        unique_together = ('user','company','component','group')
        ordering = ('user','company','component','group')
        verbose_name = 'Пользователь и Группа Организации и Компонента'
        verbose_name_plural = 'Пользователи и Группы Организаций и Компонентов'

#class ContentQuerySet(QuerySet, GroupByMixin):
#    pass

class Content(models.Model):
    #objects = ContentQuerySet.as_manager()
    name = models.CharField("Заголовок", max_length=1024)
    announcement = models.TextField("Анонс", max_length=10240, blank=True, null=True)
    description = RichTextUploadingField("Текст", blank=True, null=True)
    datebegin = models.DateTimeField("Начало")
    dateend = models.DateTimeField("Окончание")
    is_ontop = models.BooleanField("Всегда наверху", default=False)    
    type = models.ForeignKey('Dict_ContentType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='content_type', verbose_name="Тип")
    #company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='content_company', verbose_name="Организация")
    company = models.ManyToManyField('Company', related_name='content_companies', verbose_name="Организации")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    #dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_forprofile = models.BooleanField("Только для профиля", default=False)
    is_private = models.BooleanField("Приватно", default=False)
    is_active = models.BooleanField("Активность", default=True)

    def get_absolute_url(self):
        #return reverse('my_main:home')
        return reverse('my_company:content_detail', kwargs={'pk': self.pk})
    def __str__(self):
        #return (self.company.name + ' - ' + self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + ' - ' + self.type.name + ' - ' + self.name + ' - ' + self.author.username)
        return (self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + ' - ' + self.type.name + ' - ' + self.name + ' - ' + self.author.username)
    
    class Meta:
        #ordering = ('company','type','datecreate')
        ordering = ('-is_ontop','-id')
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'

class Dict_ContentType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    

    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип контента'
        verbose_name_plural = 'Типы контента'
    def __str__(self):
        return (self.name)            