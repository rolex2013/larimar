# Generated by Django 3.1.5 on 2021-06-30 12:16

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_dict_theme'),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='dateclose',
        ),
        migrations.AlterField(
            model_name='folder',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folder_children', to='files.folder', verbose_name='Папка верхнего уровня'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='theme',
            field=models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='folder_theme', to='main.dict_theme', verbose_name='Тематика'),
        ),
    ]
