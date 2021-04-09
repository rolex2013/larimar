from django.db import models

from django.urls import reverse, reverse_lazy
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey
from main.models import ModelLog

from ckeditor_uploader.fields import RichTextUploadingField

from companies.models import Company

import json
from datetime import datetime, timedelta


class Dict_ProjectStatus(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_close = models.BooleanField("Закрывает проект", default=False)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Статус проекта'
        verbose_name_plural = 'Статусы проектов'
    def __str__(self):
        return (self.name)

class Dict_ProjectStructureType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип проектов в иерархии'
        verbose_name_plural = 'Типы проектов в иерархии'
    def __str__(self):
        return (self.name)

class Dict_ProjectType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип проекта'
        verbose_name_plural = 'Типы проектов'
    def __str__(self):
        return (self.name)

class Dict_TaskStatus(models.Model):
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

class Dict_TaskStructureType(models.Model):
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

class Dict_TaskType(models.Model):
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

class Project(MPTTModel):
    name = models.CharField("Наименование", max_length=64)
    description = RichTextUploadingField("Описание")
    datebegin = models.DateField("Начало")
    dateend = models.DateField("Окончание")
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='resultcompany', verbose_name="Компания")
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_children', verbose_name="Проект верхнего уровня")
    assigner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='project_assigner', verbose_name="Исполнитель") 
    currency = models.ForeignKey('finance.Dict_Currency', on_delete=models.CASCADE, related_name='resultcurrency', verbose_name="Валюта")   
    cost = models.DecimalField("Стоимость", max_digits=12, decimal_places=2, default=0)
    percentage = models.DecimalField("Процент выполнения", max_digits=5, decimal_places=2, default=0)
    structure_type = models.ForeignKey('Dict_ProjectStructureType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_structure_type', verbose_name="Тип в иерархии")
    type = models.ForeignKey('Dict_ProjectType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_type', verbose_name="Тип")
    status = models.ForeignKey('Dict_ProjectStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_status', verbose_name="Статус")
    #docfile = models.ManyToManyField('ProjectFile', blank=True, related_name='file_project', verbose_name="Файлы")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='project_author', verbose_name="Автор")
    members = models.ManyToManyField('auth.User', related_name='project_members', verbose_name="Участники")
    is_active = models.BooleanField("Активность", default=True)    
         
    def get_absolute_url(self):
        return reverse('my_project:tasks', kwargs={'projectid': self.pk, 'pk': '0'})  
    def __str__(self):
        return (self.name + ' (' + self.datebegin.strftime('%d.%m.%Y') + '-' + self.dateend.strftime('%d.%m.%Y') + ' / ' + self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + ')')
    def save(self, *args, **kwargs):
        # Получаем старые значения для дальнейшей проверки на изменения
        old = Project.objects.filter(pk=self.pk).first() # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
        if old:
           old_name = old.name
           old_status_name = old.status.name
           old_datebegin = datetime.strftime(old.datebegin, '%Y-%m-%d')
           old_dateend = datetime.strftime(old.dateend, '%Y-%m-%d')
           old_structure_type_name = old.structure_type.name
           old_type_name = old.type.name
           old_cost = str(old.cost)
           old_currency_code_char = old.currency.code_char
           old_percentage = str(old.percentage)
           old_assigner_username = old.assigner.username
           old_is_active = old.is_active          
           #print('old_status_name='+old_status_name)        
        else:
           old_name = ''
           old_status_name = ''
           old_datebegin = ''
           old_dateend = ''
           old_structure_type_name = ''
           old_type_name = ''
           old_cost = ''
           old_currency_code_char = ''
           old_percentage = ''
           old_assigner_username = ''
           old_is_active = ''           
        #super(Project, self).save(*args, **kwargs)
        super().save(*args, **kwargs)
        self_name = self.name
        self_status_name = self.status.name
        self_datebegin = datetime.strftime(self.datebegin, '%Y-%m-%d')
        self_dateend = datetime.strftime(self.dateend, '%Y-%m-%d')
        self_structure_type_name = self.structure_type.name
        self_type_name = self.type.name
        self_cost = str(self.cost)
        self_currency_code_char = self.currency.code_char
        self_percentage = str(self.percentage)
        self_assigner_username = self.assigner.username
        self_is_active = self.is_active
        #print('self_status_name='+self_status_name)         
        # Проверка на изменения
        if self_name == old_name:
           self_name = ''
        if self_status_name == old_status_name:
           self_status_name = ''
        if self_datebegin == old_datebegin:
           self_datebegin = ''
        if self_dateend == old_dateend:
           self_dateend = ''
        if self_structure_type_name == old_structure_type_name:
           self_structure_type_name = ''
        if self_type_name == old_type_name:
           self_type_name = ''
        if self_cost == old_cost:
           self_cost = ''
        if self_currency_code_char == old_currency_code_char:
           self_currency_code_char = ''
        if self_percentage == old_percentage:
           self_percentage = ''
        if self_assigner_username == old_assigner_username:
           self_assigner_username = ''
        if self_is_active == old_is_active:
           self_is_active = ''
        if self_name or self_status_name or self_datebegin or self_dateend or self_structure_type_name or self_type_name or self_cost or self_currency_code_char or self_percentage or self_assigner_username or self_is_active != old_is_active:           
           historyjson = {"Проект":self_name, "Статус":self_status_name, 
                          "Начало":self_datebegin, "Окончание":self_dateend,
                          "Тип в иерархии":self_structure_type_name, "Тип":self_type_name,
                          "Стоимость":self_cost, "Валюта":self_currency_code_char, "Выполнен на, %":self_percentage,
                          "Исполнитель":self_assigner_username, "Активность":'✓' if self.is_active else '-' #, "Участники":self.members.username
                         }
           ModelLog.objects.create(componentname='prj', 
                                   modelname="Project",
                                   modelobjectid=self.id,
                                   author=self.author,
                                   log=json.dumps(historyjson)
                                  )                                
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

class Task(MPTTModel):
    name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Описание")
    datebegin = models.DateTimeField("Начало")
    dateend = models.DateTimeField("Окончание")
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='resultproject', verbose_name="Проект")
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='task_children', verbose_name="Задача верхнего уровня")
    assigner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='task_assigner', verbose_name="Исполнитель")   
    cost = models.DecimalField("Стоимость", max_digits=12, decimal_places=2)
    percentage = models.DecimalField("Процент выполнения", max_digits=5, decimal_places=2, default=0)    
    structure_type = models.ForeignKey('Dict_TaskStructureType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='task_structure_type', verbose_name="Тип задачи в иерархии")
    type = models.ForeignKey('Dict_TaskType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_type', verbose_name="Тип")
    status = models.ForeignKey('Dict_TaskStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_status', verbose_name="Статус")
    datecreate = models.DateTimeField("Создана", auto_now_add=True)    
    dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='resultuser', verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)
    def get_absolute_url(self):
        return reverse('my_project:taskcomments', kwargs={'taskid': self.pk})
        #return reverse('my_project:taskcomments, kwargs={'taskid': self.pk})
    def __str__(self):
         return (str(self.project) + '. ' + self.name + ' (' + self.datebegin.strftime('%d.%m.%Y, %H:%M') + ' - ' + self.dateend.strftime('%d.%m.%Y, %H:%M') + ')')
    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)          
        #TaskStatusLog.objects.create(task_id=self.id, 
        #                             status=self.status, 
        #                             author=self.author)
        historyjson = {"Задача":self.name, "Статус":self.status.name, 
                       "Начало":datetime.strftime(self.datebegin, '%Y-%m-%d'), "Окончание":datetime.strftime(self.dateend, '%Y-%m-%d'),
                       "Тип в иерархии":self.structure_type.name, "Тип":self.type.name,
                       "Стоимость":str(self.cost), "Выполнен на, %":str(self.percentage),
                       "Исполнитель":self.assigner.username, "Активность":'✓' if self.is_active else ''
                      }        
        ModelLog.objects.create(componentname='tsk', 
                                modelname="Task",
                                modelobjectid=self.id,
                                author=self.author,
                                log=json.dumps(historyjson)
                                )                                            
    class MPTTMeta:
        #order_insertion_by = ['name']    
        order_insertion_by = ['-dateend']     
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'         

class TaskComment(models.Model):
    name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Описание")
    time = models.DecimalField("Время работы, час.", max_digits=6, decimal_places=2, blank=False, null=False, default=0)
    cost = models.DecimalField("Стоимость", max_digits=9, decimal_places=2, default=0)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='resulttask', verbose_name="Задача")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)    
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True) 

    def get_absolute_url(self):
        return reverse('my_project:taskcomments', kwargs={'taskid': self.task_id})           

    def __str__(self):
        return (str(self.task) + '. ' + self.name + ' (' + self.datecreate.strftime('%d.%m.%Y, %H:%M') + ')')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class ProjectFile(models.Model):
    name = models.CharField("Наименование", null=True, blank=True, max_length=255)
    uname = models.CharField("Уникальное наименование", null=True, blank=True, max_length=255)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='project_file', verbose_name="Проект")
    pfile = models.FileField(upload_to='uploads/docs/project', blank=True, null=True, verbose_name='Файл')
    psize = models.CharField(editable=False, max_length=64)    
    datecreate = models.DateTimeField("Создан", auto_now_add=True)    
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return str(self.id) + ' ' + self.uname #file.name

"""
class ProjectStatusLog(models.Model):
    #LOG_TYPES = (('P', 'Project'), ('T', 'Task'))
    #logtype = models.CharField(max_length = 1, choices=LOG_TYPES)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='resultprojectlog', verbose_name="Проект")
    status = models.ForeignKey('Dict_ProjectStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_status_log', verbose_name="Статус Проекта")
    date = models.DateTimeField("Дата", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    description = models.CharField("Комментарий", max_length=1024)
    is_active = models.BooleanField("Активность", default=True)
    
    def __str__(self):
        return (self.project.name + '. ' + self.date.strftime('%d.%m.%Y, %H:%M') + ' - ' + self.status.name + ' (' + self.author.username + ')')
    
    class Meta:
        unique_together = ('project', 'status', 'date', 'author')
        ordering = ('project', 'date')
        verbose_name = 'История Проекта'
        verbose_name_plural = 'Истории Проектов'

class TaskStatusLog(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='resulttasklog', verbose_name="Задача")
    status = models.ForeignKey('Dict_TaskStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='task_status_log', verbose_name="Статус Задачи")
    date = models.DateTimeField("Дата", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    description = models.CharField("Комментарий", max_length=1024)
    is_active = models.BooleanField("Активность", default=True)
    
    def __str__(self):
        return (self.task.name + '. ' + self.date.strftime('%d.%m.%Y, %H:%M') + ' - ' + self.status.name + ' (' + self.author.username + ')')
    
    class Meta:
        unique_together = ('task', 'status', 'date', 'author')
        ordering = ('task', 'date')
        verbose_name = 'История Задачи'
        verbose_name_plural = 'Истории Задач'                
"""
