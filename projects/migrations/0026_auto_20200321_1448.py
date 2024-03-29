# Generated by Django 3.0.4 on 2020-03-21 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0025_auto_20200320_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='dict_projectstatus',
            name='is_close',
            field=models.BooleanField(default=False, verbose_name='Закрывает проект'),
        ),
        migrations.AddField(
            model_name='dict_taskstatus',
            name='is_close',
            field=models.BooleanField(default=False, verbose_name='Закрывает задачу'),
        ),
        migrations.AlterField(
            model_name='project',
            name='dateclose',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия'),
        ),
        migrations.AlterField(
            model_name='task',
            name='dateclose',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия'),
        ),
    ]
