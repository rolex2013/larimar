# Generated by Django 3.1.5 on 2022-01-31 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_chatmember_dateonline'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmember',
            name='is_admin',
            field=models.BooleanField(default=True, verbose_name='Администратор'),
        ),
    ]
