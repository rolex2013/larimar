# Generated by Django 3.1.5 on 2021-03-30 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0043_auto_20210330_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='docfile',
            field=models.ManyToManyField(blank=True, related_name='file_project', to='projects.ProjectFile', verbose_name='Файлы'),
        ),
    ]
