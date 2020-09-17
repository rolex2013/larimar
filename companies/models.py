from django.db import models

from django.urls import reverse, reverse_lazy
from django.utils import timezone
#import datetime

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

class Dict_PositionType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип должности'
        verbose_name_plural = 'Типы должностей'
    def __str__(self):
        return (self.name)

class Company(MPTTModel):    
    name = models.CharField("Наименование", max_length=64)
    #description = models.TextField("Описание")
    description = RichTextUploadingField("Описание")
    #company_up = models.ForeignKey('self', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='resultcompany_up', verbose_name="Головная организация")
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='company_children', verbose_name="Головная организация")
    currency = models.ForeignKey('finance.Dict_Currency', on_delete=models.CASCADE, related_name='company_currency', verbose_name="Валюта")   
    structure_type = models.ForeignKey('Dict_CompanyStructureType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='company_structure_type', verbose_name="Тип в оргструктуре")
    type = models.ForeignKey('Dict_CompanyType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='company_type', verbose_name="Тип")
    datecreate = models.DateTimeField("Создана", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)    

    def get_absolute_url(self):
        #return reverse('my_project:projects', kwargs={'companyid': self.pk, 'pk': '1'})  
        return reverse('my_company:stafflist', kwargs={'companyid': self.pk, 'pk': '1'})         
               
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

class StaffList(MPTTModel): 
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='staff_children', verbose_name="Головная должность")
    company = models.ForeignKey('Company', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='related_company', verbose_name="Организация")
    name = models.CharField("Наименование", max_length=64)
    description = models.TextField("Описание", null=True, blank=True)
    type = models.ForeignKey('Dict_PositionType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='position_type', verbose_name="Тип должности")
    currency = models.ForeignKey('finance.Dict_Currency', on_delete=models.CASCADE, related_name='related_currency', verbose_name="Валюта")
    salary = models.DecimalField("Оклад", max_digits=14, decimal_places=2)
    numberemployees = models.PositiveIntegerField("Кол-во сотрудников", default=1)
    vacancy = RichTextUploadingField("Описание вакансии", null=True, blank=True)    
    datecreate = models.DateTimeField("Создана", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_vacancy = models.BooleanField("Вакансия", default=False)
    is_active = models.BooleanField("Активность", default=True)    

    def get_absolute_url(self):
        return reverse('my_company:staffs', kwargs={'stafflistid': self.pk, 'pk': '0'})          
               
    def __str__(self):
        return (self.company.name + '. ' + self.name)
    class MPTTMeta:
        order_insertion_by = ['company', 'name']
    class Meta:
        verbose_name = 'Штатное расписание'
        verbose_name_plural = 'Штатные расписания'    

class Staff(models.Model):
    stafflist = models.ForeignKey('StaffList', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='staff_stafflist', verbose_name="Должность")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='staff_user', verbose_name="Пользователь")
    rate = models.DecimalField("Ставка (0,1 - 1)", max_digits=3, decimal_places=2, default=1)
    datebegin = models.DateField("Начало работы")
    dateend = models.DateField("Окончание работы", null=True, blank=True)    
    datecreate = models.DateTimeField("Создана", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")    
    is_active = models.BooleanField("Активность", default=True)

    def get_absolute_url(self):
        return reverse('my_company:staffs', kwargs={'stafflistid': self.stafflist.id, 'pk': '0'})  

    def __str__(self):
        return (self.stafflist.company.name + ' - ' + self.stafflist.name + ' - ' + self.user.username)

    class Meta:
        #unique_together = ('stafflist','user')
        ordering = ('stafflist','user')
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class Summary(models.Model):
    stafflist = models.ForeignKey('StaffList', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='summary_stafflist', verbose_name="Должность")
    theme = models.CharField("Тема", max_length=1024)
    candidatefirstname = models.CharField("Имя", max_length=64)
    candidatemiddlename = models.CharField("Отчество", max_length=64, blank=True, null=True)     
    candidatelastname = models.CharField("Фамилия", max_length=64)         
    email = models.CharField("E-mail", max_length=64)
    phone = models.CharField("Телефон", max_length=16)
    description = RichTextUploadingField("Описание", blank=True, null=True)
    datecreate = models.DateTimeField("Создано", auto_now_add=True)        
    #document = models.FileField(upload_to='documents/summary/')     
    is_active = models.BooleanField("Активность", default=True)

    def get_absolute_url(self):
        #return reverse('my_main:vacancy_detail', kwargs={'stafflistid': self.stafflist.id}) 
        return reverse('my_main:vacancies') 

    def __str__(self):
        middlename = self.candidatemiddlename
        if self.candidatemiddlename is None:
           middlename = ''
        return (self.stafflist.company.name + ' - ' + self.stafflist.name + ' - ' + self.candidatefirstname + ' ' + middlename + ' ' + self.candidatelastname)

    class Meta:
        #unique_together = ('stafflist','user')
        ordering = ('stafflist',)
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        

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
    #is_public = models.BooleanField("Только для внешнего сайта", default=False)
    #is_forprofile = models.BooleanField("Только для профиля", default=False)
    #is_private = models.BooleanField("Приватно", default=False)
    place = models.ForeignKey('Dict_ContentPlace', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='content_place', verbose_name="Место")    
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

class Dict_ContentPlace(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=2, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    

    class Meta:
        ordering = ('sort',)
        verbose_name = 'Место отображения контента'
        verbose_name_plural = 'Места отображения контента'
    def __str__(self):
        return (self.name)                        