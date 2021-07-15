from django.db import models

#from django.db.models import Q, Sum

from django.urls import reverse, reverse_lazy
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey
from main.models import ModelLog

from ckeditor_uploader.fields import RichTextUploadingField

from companies.models import Company

class Dict_System(models.Model):
    code = models.CharField("Код системы", max_length=128)
    name = models.CharField("Наименование системы", max_length=128)
    domain = models.CharField("Наименование домена", max_length=64, blank=True, null=True)
    url = models.CharField("url", max_length=128)
    ip = models.CharField("ip-адрес", max_length=15, blank=True, null=True)
    email = models.CharField("Контактный e-mail", max_length=15, blank=True, null=True)
    phone = models.CharField("Контактный телефон", max_length=15, blank=True, null=True)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=128, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Система'
        verbose_name_plural = 'Системы'
    def __str__(self):
        return (self.name)

class Dict_FeedbackTicketStatus(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_close = models.BooleanField("Закрывает тикет", default=False)
    is_active = models.BooleanField("Активность", default=True)
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Статус тикета'
        verbose_name_plural = 'Статусы тикетов'
    def __str__(self):
        return (self.name)

class Dict_FeedbackTaskStatus(models.Model):
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

class FeedbackTicket(models.Model):
    name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Описание")
    #datebegin = models.DateTimeField("Начало")
    #dateend = models.DateTimeField("Окончание")
    system = models.ForeignKey('Dict_System', on_delete=models.CASCADE, related_name='feedback_system',
                                verbose_name="Система")
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='feedback_company',
                                verbose_name="Компания")
    #assigner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='task_assigner', verbose_name="Исполнитель")
    #cost = models.DecimalField("Стоимость", max_digits=12, decimal_places=2)
    #percentage = models.DecimalField("Процент выполнения", max_digits=5, decimal_places=2, default=0)
    #structure_type = models.ForeignKey('Dict_TaskStructureType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='task_structure_type', verbose_name="Тип задачи в иерархии")
    #type = models.ForeignKey('Dict_TaskType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_type', verbose_name="Тип")
    status = models.ForeignKey('Dict_FeedbackTicketStatus', limit_choices_to={'is_active': True}, on_delete=models.CASCADE, related_name='feedback_ticketstatus', verbose_name="Статус")
    datecreate = models.DateTimeField("Создана", auto_now_add=True)
    dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='feedback_ticket_user', verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)
    """
    @property
    # суммарная стоимость по Комментариям (сколько освоено средств)
    def costsum(self):
        return TicketComment.objects.filter(task_id=self.id).aggregate(Sum('cost'))
    @property
    # суммарная затраченное время по Комментариям
    def timesum(self):
        return TaskComment.objects.filter(task_id=self.id).aggregate(Sum('time'))
    """

    def get_absolute_url(self):
        return reverse('my_feedback:ticketcomments', kwargs={'taskid': self.pk})
    def __str__(self):
        return (self.name + ' (' + self.datecreate.strftime('%d.%m.%Y, %H:%M') + ')')
    class MPTTMeta:
        order_insertion_by = ['-datecreate']
    class Meta:
        verbose_name = 'Тикет'
        verbose_name_plural = 'Тикеты'

class FeedbackTask(MPTTModel):
    name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Описание")
    datebegin = models.DateTimeField("Начало")
    dateend = models.DateTimeField("Окончание")
    ticket = models.ForeignKey('FeedbackTicket', on_delete=models.CASCADE, related_name='resultticket', verbose_name="Тикет")
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='task_children', verbose_name="Задача верхнего уровня")
    assigner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='ticket_task_assigner', verbose_name="Исполнитель")
    cost = models.DecimalField("Стоимость", max_digits=12, decimal_places=2)
    percentage = models.DecimalField("Процент выполнения", max_digits=5, decimal_places=2, default=0)
    #structure_type = models.ForeignKey('Dict_TaskStructureType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='task_structure_type', verbose_name="Тип задачи в иерархии")
    #type = models.ForeignKey('Dict_TaskType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='project_type', verbose_name="Тип")
    status = models.ForeignKey('Dict_FeedbackTaskStatus', limit_choices_to={'is_active': True}, on_delete=models.CASCADE, related_name='feedback_taskstatus', verbose_name="Статус")
    datecreate = models.DateTimeField("Создана", auto_now_add=True)
    dateclose = models.DateTimeField("Дата закрытия", auto_now_add=False, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='feedback_task_user', verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)

    @property
    # суммарная стоимость по Комментариям (сколько освоено средств)
    def costsum(self):
        return FeedbackTaskComment.objects.filter(task_id=self.id).aggregate(Sum('cost'))
    @property
    # суммарная затраченное время по Комментариям
    def timesum(self):
        return FeedbackTaskComment.objects.filter(task_id=self.id).aggregate(Sum('time'))

    def get_absolute_url(self):
        return reverse('my_feedback:taskcomments', kwargs={'taskid': self.pk})
        #return reverse('my_project:taskcomments, kwargs={'taskid': self.pk})
    def __str__(self):
         return (str(self.ticket) + '. ' + self.name + ' (' + self.datebegin.strftime('%d.%m.%Y, %H:%M') + ' - ' + self.dateend.strftime('%d.%m.%Y, %H:%M') + ')')
    class MPTTMeta:
        #order_insertion_by = ['name']
        order_insertion_by = ['-dateend']
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

class FeedbackTicketComment(models.Model):
    name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Описание")
    time = models.DecimalField("Время работы, час.", max_digits=6, decimal_places=2, blank=False, null=False, default=0)
    cost = models.DecimalField("Стоимость", max_digits=9, decimal_places=2, default=0)
    ticket = models.ForeignKey('FeedbackTicket', on_delete=models.CASCADE, related_name='feedback_ticket', verbose_name="Тикет")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)

    def get_absolute_url(self):
        return reverse('my_ticket:feedbacktaskcomments', kwargs={'taskid': self.ticket_id})

    def __str__(self):
        return (str(self.ticket) + '. ' + self.name + ' (' + self.datecreate.strftime('%d.%m.%Y, %H:%M') + ')')

    @property
    def files(self):
        return FeedbackFile.objects.filter(taskcomment_id=self.id, is_active=True)

    class Meta:
        verbose_name = 'Комментарий тикета'
        verbose_name_plural = 'Комментарии тикетов'

class FeedbackTaskComment(models.Model):
    name = models.CharField("Наименование", max_length=128)
    description = RichTextUploadingField("Описание")
    time = models.DecimalField("Время работы, час.", max_digits=6, decimal_places=2, blank=False, null=False, default=0)
    cost = models.DecimalField("Стоимость", max_digits=9, decimal_places=2, default=0)
    task = models.ForeignKey('FeedbackTask', on_delete=models.CASCADE, related_name='resulttask', verbose_name="Задача")
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)

    def get_absolute_url(self):
        return reverse('my_feedback:feedbacktaskcomments', kwargs={'taskid': self.task_id})

    def __str__(self):
        return (str(self.task) + '. ' + self.name + ' (' + self.datecreate.strftime('%d.%m.%Y, %H:%M') + ')')

    @property
    def files(self):
        return FeedbackFile.objects.filter(taskcomment_id=self.id, is_active=True)

    class Meta:
        verbose_name = 'Комментарий задачи'
        verbose_name_plural = 'Комментарии задач'

class FeedbackFile(models.Model):
    name = models.CharField("Наименование", null=True, blank=True, max_length=255)
    uname = models.CharField("Уникальное наименование", null=True, blank=True, max_length=255)
    ticket = models.ForeignKey('FeedbackTicket', null=True, blank=True, on_delete=models.CASCADE, related_name='feedbackticket_file', verbose_name="Тикет")
    ticketcomment = models.ForeignKey('FeedbackTicketComment', null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='ticketcomment_file', verbose_name="Комментарий тикета")
    task = models.ForeignKey('FeedbackTask', null=True, blank=True, on_delete=models.CASCADE, related_name='feedbacktask_file', verbose_name="Задача")
    taskcomment = models.ForeignKey('FeedbackTaskComment', null=True, blank=True, on_delete=models.CASCADE, related_name='feedbacktaskcomment_file', verbose_name="Комментарий задачи")
    pfile = models.FileField(upload_to='uploads/files/feedback', blank=True, null=True, verbose_name='Файл')
    psize = models.PositiveIntegerField(editable=False, null=True, blank=True)
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return str(self.id) + ' ' + self.uname #file.name

