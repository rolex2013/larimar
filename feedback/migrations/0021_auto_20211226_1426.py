# Generated by Django 3.1.5 on 2021-12-26 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0020_auto_20211224_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackticket',
            name='requeststatuscode',
            field=models.IntegerField(blank=True, null=True, verbose_name='Код завершения операции'),
        ),
        migrations.AddField(
            model_name='feedbackticketcomment',
            name='requeststatuscode',
            field=models.IntegerField(blank=True, null=True, verbose_name='Код завершения операции'),
        ),
    ]
