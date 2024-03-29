# Generated by Django 3.1.5 on 2021-04-14 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0051_auto_20210412_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectfile',
            name='pfile',
            field=models.FileField(blank=True, null=True, upload_to='uploads/files/project', verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='taskcomment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taskcomment_file', to='projects.taskcomment', verbose_name='Комментарий'),
        ),
    ]
