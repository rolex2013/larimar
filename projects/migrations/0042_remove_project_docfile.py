# Generated by Django 3.1.5 on 2021-03-22 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_project_docfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='docfile',
        ),
    ]
