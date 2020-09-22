# Generated by Django 3.0.5 on 2020-05-26 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dict_Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_char', models.CharField(max_length=3, verbose_name='Символьный код')),
                ('code_num', models.CharField(max_length=3, verbose_name='Цифровой код')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование')),
                ('shortname', models.CharField(max_length=24, verbose_name='Краткое наименование')),
                ('sort', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
                ('name_lang', models.CharField(blank=True, max_length=64, null=True, verbose_name='Перевод')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Вид валюты',
                'verbose_name_plural': 'Виды валют',
                'ordering': ('sort',),
            },
        ),
    ]