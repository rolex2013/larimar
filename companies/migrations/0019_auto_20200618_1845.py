# Generated by Django 3.0.6 on 2020-06-18 15:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0006_auto_20200618_1813'),
        ('companies', '0018_auto_20200618_1826'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Staff',
            new_name='StaffList',
        ),
    ]
