# Generated by Django 3.1.5 on 2022-03-30 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0005_auto_20220203_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmember',
            name='dateoffline',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Момент выхода из чата'),
        ),
    ]