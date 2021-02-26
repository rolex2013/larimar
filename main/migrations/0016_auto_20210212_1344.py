# Generated by Django 3.1.5 on 2021-02-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_modellog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modellog',
            options={'ordering': ('componentname', 'modelname', 'modelobjectid', 'date'), 'verbose_name': 'История Объекта', 'verbose_name_plural': 'Истории Объектов'},
        ),
        migrations.AddField(
            model_name='modellog',
            name='modelobjectid',
            field=models.IntegerField(default=17, verbose_name='Объект'),
            preserve_default=False,
        ),
    ]