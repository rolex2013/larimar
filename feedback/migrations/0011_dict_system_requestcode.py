# Generated by Django 3.1.5 on 2021-11-05 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0010_feedbackticketcomment_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='dict_system',
            name='requestcode',
            field=models.IntegerField(blank=True, null=True, verbose_name='Код завершения операции'),
        ),
    ]
