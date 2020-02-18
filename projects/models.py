from django.db import models

from django.urls import reverse
from django.utils import timezone

#now = timezone.now()
#now.strftime('%H:%M:%S')

class Project(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    datebegin = models.DateField()
    dateend = models.DateField()
    assigner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='project_assigner')
    datecreate = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    #def get_update_url(self):
    #    return reverse('project_update ', kwargs={'pk': self.pk})

    def __str__(self):
    #     return (self.name + ' (' + timezone.localtime(now).self.datebegin.strftime('%d.%m.%Y') + ' - ' + timezone.localtime(now).self.dateend.strftime('%d.%m.%Y') + ')')
          return (self.name + ' (' + self.datebegin.strftime('%d.%m.%Y') + ' - ' + self.dateend.strftime('%d.%m.%Y') + ')')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

class Task(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='resultproject')
    datebegin = models.DateTimeField()
    dateend = models.DateTimeField()
    assigner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='task_assigner')    
    datecreate = models.DateTimeField(auto_now_add=True)    
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='resultuser')

    def __str__(self):
         return (str(self.project) + '. ' + self.name + ' (' + self.datebegin.strftime('%d.%m.%Y, %H:%M') + ' - ' + self.dateend.strftime('%d.%m.%Y, %H:%M') + ')')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'         

class TaskComment(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='resulttask')
    #date = models.DateTimeField()
    datecreate = models.DateTimeField(auto_now_add=True)    
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)    

    def __str__(self):
         return (str(self.task) + '. ' + self.name + ' (' + self.datecreate.strftime('%d.%m.%Y, %H:%M') + ')')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'