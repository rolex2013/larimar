from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField


class Dict_ProtocolType(models.Model):
    name = models.CharField("Наименование", max_length=64)
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Протокол оповещения'
        verbose_name_plural = 'Протоколы оповещений'
    def __str__(self):
        return (self.name)


class Component(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='component_children', verbose_name="Головной компонент")
    name = models.CharField("Наименование", max_length=64)
    #description = RichTextUploadingField("Описание")
    description = models.CharField("Описание", max_length=256, blank=True, null=True)
    menu = models.CharField("Пункт меню", max_length=256, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    

    #def get_absolute_url(self):
    #    return reverse('my_main:components', kwargs={'componentid': self.pk, 'pk': '1'})          
               
    def __str__(self):
        return (self.name)

    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'


class Notification(models.Model):
    datecreate = models.DateTimeField("Дата", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    type = models.ForeignKey('Dict_ProtocolType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='protocol_type', verbose_name="Тип")
    sendfrom = models.CharField("От кого", max_length=64, blank=True, null=True)  
    theme = models.CharField("Тема", max_length=256, blank=True, null=True) 
    text = RichTextUploadingField("Текст", max_length=1024)      
    recipient = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, related_name='notify_recipient', verbose_name="Получатель")     
    sendto = models.CharField("Кому", max_length=64, blank=True, null=True)
    datesent = models.DateTimeField("Момент отправки", auto_now_add=False, blank=True, null=True)
    dateread = models.DateTimeField("Момент прочтения", auto_now_add=False, blank=True, null=True)    
    response = models.CharField("Ответ", max_length=128, blank=True, null=True) 
    is_sent = models.BooleanField("Отправлено", default=False)
    is_read = models.BooleanField("Прочитано", default=False)           
    is_active = models.BooleanField("Активность", default=True)      
               
    def __str__(self):
        return (self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + ' | ' + self.theme + ' | ' + self.author.username)

    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'