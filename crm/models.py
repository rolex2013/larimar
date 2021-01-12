from django.db import models

from django.urls import reverse, reverse_lazy
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from ckeditor_uploader.fields import RichTextUploadingField

from companies.models import Company


class Dict_ClientType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    description = models.TextField("Описание", blank=True, null=True) 
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип клиента'
        verbose_name_plural = 'Типы клиентов'
    def __str__(self):
        return (self.name)

class Dict_ClientStatus(models.Model):
    name = models.CharField("Наименование", max_length=64)
    description = models.TextField("Описание", blank=True, null=True) 
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Статус клиента'
        verbose_name_plural = 'Статусы клиентов'
    def __str__(self):
        return (self.name)        

class Client(models.Model):
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='result_company_client', verbose_name="Организация")    
    manager = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='result_manager_client', verbose_name="Менеджер")    
    user = models.OneToOneField('auth.User', blank=True, null=True, on_delete=models.CASCADE, related_name='result_user_client', verbose_name="Пользователь")
    is_notify = models.BooleanField("Оповещать", default=False)
    protocoltype = models.ForeignKey('main.Dict_ProtocolType', blank=True, null=True, on_delete=models.CASCADE, related_name='result_protocoltype_client', verbose_name="Протокол оповещения")    
    type = models.ForeignKey('Dict_ClientType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='client_type_client', verbose_name="Тип клиента")
    status = models.ForeignKey('Dict_ClientStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='client_status_client', verbose_name="Статус клиента")    
    firstname = models.CharField("Имя", max_length=64)
    middlename = models.CharField("Отчество", blank=True, null=True, max_length=64)
    lastname = models.CharField("Фамилия", max_length=64)
    email = models.CharField("E-mail", max_length=64, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=16, blank=True, null=True)
    #description = models.TextField("Описание")    
    description = RichTextUploadingField("Описание", blank=True, null=True)
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='client_author', verbose_name="Автор")
    members = models.ManyToManyField('auth.User', related_name='client_members', verbose_name="Участники")        
    is_active = models.BooleanField("Активность", default=True)

    def get_absolute_url(self):
        #return reverse('my_crm:client_detail', kwargs={'userid': self.user.pk, 'param': ' '})  
        return reverse('my_crm:clients0')  
    def __str__(self):
        #return (self.user.username + ' - ' + self.company.name)
        #return (self.user.username)
        return (self.firstname + ' ' + self.middlename +' ' + self.lastname)
    class Meta:
        #unique_together = ('user','company')
        #ordering = ('user')
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
