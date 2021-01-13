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

class Dict_ClientTaskStatus(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_close = models.BooleanField("Закрывает задачу", default=False)    
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задач'
    def __str__(self):
        return (self.name)

class Dict_ClientTaskStructureType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип задачи в иерархии'
        verbose_name_plural = 'Типы задач в иерархии'
    def __str__(self):
        return (self.name)

class Dict_ClientTaskType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'
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
        return reverse('my_crm:tasks', kwargs={'clientid': self.pk, 'pk': '0'}) 
        #return reverse('my_crm:clients0')  
    def __str__(self):
        #return (self.user.username + ' - ' + self.company.name)
        #return (self.user.username)
        return (self.firstname + ' ' + self.middlename +' ' + self.lastname)
    class Meta:
        #unique_together = ('user','company')
        #ordering = ('user')
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class ClientTask(MPTTModel):
    name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Описание")
    datebegin = models.DateTimeField("Начало")
    dateend = models.DateTimeField("Окончание")
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='resultclient', verbose_name="Клиент")
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='task_children', verbose_name="Задача верхнего уровня")
    assigner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='clienttask_assigner', verbose_name="Исполнитель")   
    cost = models.DecimalField("Стоимость", max_digits=12, decimal_places=2)
    percentage = models.DecimalField("Процент выполнения", max_digits=5, decimal_places=2, default=0)    
    structure_type = models.ForeignKey('Dict_ClientTaskStructureType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='clienttask_structure_type', verbose_name="Тип задачи в иерархии")
    type = models.ForeignKey('Dict_ClientTaskType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='clienttask_type', verbose_name="Тип")
    status = models.ForeignKey('Dict_ClientTaskStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='clienttask_status', verbose_name="Статус")
    datecreate = models.DateTimeField("Создана", auto_now_add=True)    
    dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='resultclienttaskuser', verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)
    def get_absolute_url(self):
        return reverse('my_crm:taskcomments', kwargs={'taskid': self.pk})
        #return reverse('my_project:taskcomments, kwargs={'taskid': self.pk})
    def __str__(self):
         return (str(self.client) + '. ' + self.name + ' (' + self.datebegin.strftime('%d.%m.%Y, %H:%M') + ' - ' + self.dateend.strftime('%d.%m.%Y, %H:%M') + ')')
    class MPTTMeta:
        #order_insertion_by = ['name']    
        order_insertion_by = ['-dateend']     
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'         

class ClientTaskComment(models.Model):
    name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Описание")
    time = models.DecimalField("Время работы, час.", max_digits=6, decimal_places=2, blank=False, null=False, default=0)
    cost = models.DecimalField("Стоимость", max_digits=9, decimal_places=2, default=0)
    task = models.ForeignKey('ClientTask', on_delete=models.CASCADE, related_name='resultclienttask', verbose_name="Задача")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)    
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True) 

    def get_absolute_url(self):
        return reverse('my_crm:taskcomments', kwargs={'taskid': self.task_id})           

    def __str__(self):
        return (str(self.task) + '. ' + self.name + ' (' + self.datecreate.strftime('%d.%m.%Y, %H:%M') + ')')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class ClientStatusLog(models.Model):
    #LOG_TYPES = (('P', 'Client'), ('T', 'Task'))
    #logtype = models.CharField(max_length = 1, choices=LOG_TYPES)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='resultclientlog', verbose_name="Проект")
    status = models.ForeignKey('Dict_ClientStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='client_status_log', verbose_name="Статус Клиента")
    date = models.DateTimeField("Дата", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    description = models.CharField("Комментарий", max_length=1024)
    is_active = models.BooleanField("Активность", default=True)
    
    def __str__(self):
        return (self.client.name + '. ' + self.date.strftime('%d.%m.%Y, %H:%M') + ' - ' + self.status.name + ' (' + self.author.username + ')')
    
    class Meta:
        unique_together = ('client', 'status', 'date', 'author')
        ordering = ('client', 'date')
        verbose_name = 'История Клиента'
        verbose_name_plural = 'Истории Клиентов'

class ClientTaskStatusLog(models.Model):
    task = models.ForeignKey('ClientTask', on_delete=models.CASCADE, related_name='resultclienttasklog', verbose_name="Задача")
    status = models.ForeignKey('Dict_ClientTaskStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='clienttask_status_log', verbose_name="Статус Задачи")
    date = models.DateTimeField("Дата", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    description = models.CharField("Комментарий", max_length=1024)
    is_active = models.BooleanField("Активность", default=True)
    
    def __str__(self):
        return (self.clienttask.name + '. ' + self.date.strftime('%d.%m.%Y, %H:%M') + ' - ' + self.status.name + ' (' + self.author.username + ')')
    
    class Meta:
        unique_together = ('task', 'status', 'date', 'author')
        ordering = ('task', 'date')
        verbose_name = 'История Задачи'
        verbose_name_plural = 'Истории Задач'                
        
