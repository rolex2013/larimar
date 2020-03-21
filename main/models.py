from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

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

