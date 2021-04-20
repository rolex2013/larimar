from django.db import models

from django.urls import reverse, reverse_lazy
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey
from main.models import ModelLog

from ckeditor_uploader.fields import RichTextUploadingField

from companies.models import Company

import json
from datetime import datetime, timedelta
#import pytz


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
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='project_author', verbose_name="Автор")
    members = models.ManyToManyField('auth.User', related_name='project_members', verbose_name="Участники")
    is_active = models.BooleanField("Активность", default=True)    
         
    def get_absolute_url(self):
        return reverse('my_project:tasks', kwargs={'projectid': self.pk, 'pk': '0'})  
    def __str__(self):
        return (self.name + ' (' + self.datebegin.strftime('%d.%m.%Y') + '-' + self.dateend.strftime('%d.%m.%Y') + ' / ' + self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + ')')
    """
    def save(self, *args, **kwargs):
        # Получаем старые значения для дальнейшей проверки на изменения
        old = Project.objects.filter(pk=self.pk).first() # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
        super().save(*args, **kwargs)
        if old:
           historyjson = {"Проект":'' if self.name == old.name else self.name,
                          "Статус":'' if self.status.name == old.status.name else self.status.name, 
                          "Начало":'' if self.datebegin == old.datebegin else self.datebegin.strftime('%d.%m.%Y'), 
                          "Окончание":'' if self.dateend == old.dateend else self.dateend.strftime('%d.%m.%Y'),
                          "Тип в иерархии":'' if self.structure_type.name == old.structure_type.name else self.structure_type.name,
                          "Тип":'' if self.type.name == old.type.name else self.type.name,
                          "Стоимость":'' if self.cost == old.cost else str(self.cost),
                          "Валюта":'' if self.currency.code_char == old.currency.code_char else str(self.currency.code_char),
                          "Выполнен на, %":'' if self.percentage == old.percentage else str(self.percentage),
                          "Исполнитель":'' if self.assigner.username == old.assigner.username else self.assigner.username,
                          "Активность":'' if self.is_active == old.is_active else '✓' if self.is_active else '-'
                          #, "Участники":self.members.username
                         }                                     
        else:
           historyjson = {"Проект": self.name,
                          "Статус": self.status.name, 
                          "Начало": self.datebegin.strftime('%d.%m.%Y'), 
                          "Окончание": self.dateend.strftime('%d.%m.%Y'),
                          "Тип в иерархии": self.structure_type.name,
                          "Тип": self.type.name,
                          "Стоимость": str(self.cost),
                          "Валюта": str(self.currency.code_char),
                          "Выполнен на, %": str(self.percentage),
                          "Исполнитель": self.assigner.username,
                          "Активность": '✓' if self.is_active else '-'
                          #, "Участники":self.members.username
                         }                                     
        ModelLog.objects.create(componentname='prj', modelname="Project", modelobjectid=self.id, author=self.author, log=json.dumps(historyjson))
    """                               
    #class MPTTMeta:
    #    order_insertion_by = ['name']
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

    @property
    def files(self):
        return ProjectFile.objects.filter(taskcomment_id=self.id, is_active=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class ProjectFile(models.Model):
    name = models.CharField("Наименование", null=True, blank=True, max_length=255)
    uname = models.CharField("Уникальное наименование", null=True, blank=True, max_length=255)
    project = models.ForeignKey('Project', null=True, blank=True, on_delete=models.CASCADE, related_name='project_file', verbose_name="Проект")
    task = models.ForeignKey('Task', null=True, blank=True, on_delete=models.CASCADE, related_name='task_file', verbose_name="Задача")
    taskcomment = models.ForeignKey('TaskComment', null=True, blank=True, on_delete=models.CASCADE, related_name='taskcomment_file', verbose_name="Комментарий")        
    pfile = models.FileField(upload_to='uploads/files/project', blank=True, null=True, verbose_name='Файл')
    psize = models.CharField(editable=False, max_length=64)    
    datecreate = models.DateTimeField("Создан", auto_now_add=True)    
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return str(self.id) + ' ' + self.uname #file.name

