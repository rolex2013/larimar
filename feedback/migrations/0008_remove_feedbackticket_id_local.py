# Generated by Django 3.1.5 on 2021-09-02 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0007_feedbackticket_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackticket',
            name='id_local',
        ),
    ]