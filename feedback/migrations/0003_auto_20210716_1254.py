# Generated by Django 3.1.5 on 2021-07-16 09:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20210716_1223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dict_system',
            options={'verbose_name': 'Система', 'verbose_name_plural': 'Системы'},
        ),
        migrations.RemoveField(
            model_name='dict_system',
            name='name_lang',
        ),
        migrations.RemoveField(
            model_name='dict_system',
            name='sort',
        ),
        migrations.RemoveField(
            model_name='feedbackticket',
            name='dateclose',
        ),
        migrations.RemoveField(
            model_name='feedbackticket',
            name='datecreate',
        ),
        migrations.AddField(
            model_name='dict_system',
            name='dateclose',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия'),
        ),
        migrations.AddField(
            model_name='dict_system',
            name='datecreate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Создана'),
            preserve_default=False,
        ),
    ]
