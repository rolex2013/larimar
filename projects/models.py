from django.db import models

from django.urls import reverse, reverse_lazy
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from ckeditor_uploader.fields import RichTextUploadingField

from companies.models import Company


class Dict_ProjectStatus(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
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
    structure_type = models.ForeignKey('Dict_ProjectStructureType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_structure_type', verbose_name="Тип проекта в иерархии")
    type = models.ForeignKey('Dict_ProjectType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_type', verbose_name="Тип")
    status = models.ForeignKey('Dict_ProjectStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_status', verbose_name="Статус")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    dateclose = models.DateTimeField("Закрыт", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)    
         
    def get_absolute_url(self):
        return reverse('my_project:tasks', kwargs={'projectid': self.pk, 'pk': '0'})  
    def __str__(self):
        return (self.name + ' (' + self.datebegin.strftime('%d.%m.%Y') + '-' + self.dateend.strftime('%d.%m.%Y') + ' / ' + self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + ')')

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
    structure_type = models.ForeignKey('Dict_TaskStructureType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='task_structure_type', verbose_name="Тип задачи в иерархии")
    type = models.ForeignKey('Dict_TaskType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_type', verbose_name="Тип")
    status = models.ForeignKey('Dict_TaskStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_status', verbose_name="Статус")
    datecreate = models.DateTimeField("Создана", auto_now_add=True)    
    dateclose = models.DateTimeField("Закрыта", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='resultuser', verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)
    def get_absolute_url(self):
        return reverse('my_project:task_detail', kwargs={'pk': self.pk})
    def __str__(self):
         return (str(self.project) + '. ' + self.name + ' (' + self.datebegin.strftime('%d.%m.%Y, %H:%M') + ' - ' + self.dateend.strftime('%d.%m.%Y, %H:%M') + ')')
    class MPTTMeta:
        order_insertion_by = ['name']         
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'         

class TaskComment(models.Model):
    name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Описание")
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='resulttask', verbose_name="Задача")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)    
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True) 

    def get_absolute_url(self):
        return reverse('my_project:task_detail', kwargs={'pk': self.task_id})           

    def __str__(self):
        return (str(self.task) + '. ' + self.name + ' (' + self.datecreate.strftime('%d.%m.%Y, %H:%M') + ')')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

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