# Generated by Django 3.0.2 on 2020-02-17 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_auto_20200217_1947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='company_up',
            new_name='parent',
        ),
    ]
