from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField


class Meta_Param(models.Model):
    name = models.CharField("Наименование", max_length=64)
    datecreate = models.DateTimeField("Дата", auto_now_add=True)
    # *** если is_service==True, то доступна регистрация Организаций пользователями и тестирование Системы в мультипользовательском режиме ***
    is_service = models.BooleanField("Система, как сервис", default=True) 
    is_active = models.BooleanField("Активность Системы", default=True) 
    class Meta:
        ordering = ('datecreate',)     
    def __str__(self):
        return (self.datecreate.strftime('%d.%m.%Y %H:%M:%S') + '|' + self.name)      

class Meta_ObjectType(models.Model):
    shortname = models.CharField("Код", max_length=16)
    name = models.CharField("Наименование", max_length=64)
    tablename = models.CharField("Таблица", max_length=64)    
    sort = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    name_lang = models.CharField("Перевод", max_length=64, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Список типов объектов'
        verbose_name_plural = 'Списки типов объектов'
    def __str__(self):
        return (self.name)

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
    objecttype = models.ForeignKey('Meta_ObjectType', limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='meta_objecttype', verbose_name="Тип Объекта")
    objectid = models.PositiveIntegerField("ID объекта", default=0) 
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

class ModelLog(models.Model):
    #LOG_TYPES = (('P', 'Project'), ('T', 'Task'))
    #logtype = models.CharField(max_length = 1, choices=LOG_TYPES)
    componentname = models.CharField("Компонент", max_length=16)
    modelname = models.CharField("Модель", max_length=64)
    modelobjectid = models.IntegerField("Объект")
    date = models.DateTimeField("Дата", auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    log = models.TextField()
    is_active = models.BooleanField("Активность", default=True)
    
    def __str__(self):
        return (self.componentname + '. ' + self.modelname + self.date.strftime('%d.%m.%Y, %H:%M') + ' (' + self.author.username + ')' + self.log)
    
    class Meta:
        #unique_together = ('project', 'status', 'date', 'author')
        ordering = ('componentname', 'modelname', 'modelobjectid', 'date')
        verbose_name = 'История Объекта'
        verbose_name_plural = 'Истории Объектов'

class Menu(models.Model):
    name = models.CharField("Наименование", max_length=128)
    slug = models.CharField("slug", max_length=64)
    base_url = models.CharField("Основной URL", max_length=128)
    description = models.TextField("Описание", blank=True, null=True)
    #sort = models.PositiveSmallIntegerField(default=5, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)            
    
    def __str__(self):
        return (self.name)
    
    class Meta:
        #ordering = 'sort'
        verbose_name = 'Список меню'
        verbose_name_plural = 'Списки меню'

class MenuItem(MPTTModel):    
    title = models.CharField("Наименование", max_length=128)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='menuitem_menu', verbose_name="Меню")
    component = models.ForeignKey('Component', null=True, blank=True, on_delete=models.CASCADE, related_name='menuitem_component', verbose_name="Компонент")
    description = models.TextField("Описание", null=True, blank=True)
    link_url = models.CharField("URL", max_length=128)
    parent = TreeForeignKey('self', null=True, blank=True, limit_choices_to={'is_active':True}, on_delete=models.CASCADE, related_name='menuitem_children', verbose_name="Головной пункт меню")
    sort = models.PositiveSmallIntegerField(default=5, blank=True, null=True)
    is_active = models.BooleanField("Активность", default=True)    
                      
    def __str__(self):
        return (self.menu.name + ' ' + self.title)
    class MPTTMeta:
        #order_insertion_by = ['title']
        order_insertion_by = ['sort']
    class Meta:
        #ordering = ('menu', 'sort')
        verbose_name = 'Пункты меню'
        verbose_name_plural = 'Пункты меню'        
