# Generated by Django 3.1.5 on 2021-01-27 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0013_auto_20210127_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='initiator',
        ),
    ]