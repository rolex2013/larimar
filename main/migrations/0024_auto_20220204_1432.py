# Generated by Django 3.1.5 on 2022-02-04 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_dict_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='code',
            field=models.CharField(default='chats', max_length=64, verbose_name='Код'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='component',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Наименование'),
        ),
    ]
