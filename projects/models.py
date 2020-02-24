from django.db import models

from django.urls import reverse, reverse_lazy
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

#now = timezone.now()
#now.strftime('%H:%M:%S')

class Dict_CompanyType(models.Model):
    name = models.CharField("Наименование", max_length=32)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=256, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип организации'
        verbose_name_plural = 'Типы организации'
    def __str__(self):
        return (self.name)

class Dict_ProjectStatus(models.Model):
    name = models.CharField("Наименование", max_length=32)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=256, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Статус проекта'
        verbose_name_plural = 'Статусы проекта'
    def __str__(self):
        return (self.name)

class Dict_ProjectType(models.Model):
    name = models.CharField("Наименование", max_length=32)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=256, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип проекта'
        verbose_name_plural = 'Типы проекта'
    def __str__(self):
        return (self.name)

class Dict_TaskStatus(models.Model):
    name = models.CharField("Наименование", max_length=32)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=256, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задачи'
    def __str__(self):
        return (self.name)

class Dict_TaskType(models.Model):
    name = models.CharField("Наименование", max_length=32)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=256, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задачи'
    def __str__(self):
        return (self.name)


#class Company(models.Model):
class Company(MPTTModel):    
    name = models.CharField("Наименование", max_length=64)
    description = models.TextField("Описание")
    #company_up = models.ForeignKey('self', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='resultcompany_up', verbose_name="Головная организация")
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='company_children', verbose_name="Головная организация")
    type = models.ForeignKey('Dict_CompanyType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='company_type', verbose_name="Тип")
    datecreate = models.DateTimeField("Создана", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)    
    #def get_create_url(self):
    #    #return reverse('my_project:company_detail', kwargs={'pk': self.pk})  
    #    return reverse('my_project:companies', kwargs={'pk': self.pk})
    #def get_update_url(self):
    #    return reverse('my_project:projects', kwargs={'companyid': self.pk, 'pk': self.resultcompany.all()[0].id})          
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

class Project(MPTTModel):
    name = models.CharField("Наименование", max_length=64)
    description = models.TextField("Описание")
    datebegin = models.DateField("Начало")
    dateend = models.DateField("Окончание")
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='resultcompany', verbose_name="Компания")    
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_children', verbose_name="Проект верхнего уровня")
    assigner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='project_assigner', verbose_name="Исполнитель")    
    type = models.ForeignKey('Dict_ProjectType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_type', verbose_name="Тип")
    status = models.ForeignKey('Dict_ProjectStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_status', verbose_name="Статус")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)    
    #def get_create_url(self):
    #    #return reverse('my_project:company_detail')
    #    return reverse('my_project:projects')          
    def get_absolute_url(self):
        #return reverse('my_project:project_detail', kwargs={'pk': self.pk})
        #companyid = self.company_id
        #return reverse('my_project:projects', kwargs={'companyid': self.company_id, 'pk': self.pk})
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
    description = models.TextField("Описание")
    datebegin = models.DateTimeField("Начало")
    dateend = models.DateTimeField("Окончание")
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='resultproject', verbose_name="Проект")
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='task_children', verbose_name="Задача верхнего уровня")
    assigner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='task_assigner', verbose_name="Исполнитель")   
    type = models.ForeignKey('Dict_TaskType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_type', verbose_name="Тип")
    status = models.ForeignKey('Dict_TaskStatus', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_status', verbose_name="Статус")
    datecreate = models.DateTimeField("Создано", auto_now_add=True)    
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='resultuser', verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)
    def get_absolute_url(self):
        return reverse('my_project:task_detail', kwargs={'pk': self.pk})
        #return reverse('my_project:tasks', kwargs={'projectid': self.project, 'pk': self.pk})
    def __str__(self):
         return (str(self.project) + '. ' + self.name + ' (' + self.datebegin.strftime('%d.%m.%Y, %H:%M') + ' - ' + self.dateend.strftime('%d.%m.%Y, %H:%M') + ')')
    class MPTTMeta:
        order_insertion_by = ['name']         
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'         

class TaskComment(models.Model):
    name = models.CharField("Наименование", max_length=128)
    description = models.TextField("Описание")
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