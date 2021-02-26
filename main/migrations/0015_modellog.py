# Generated by Django 3.1.5 on 2021-02-12 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0014_auto_20200523_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('componentname', models.CharField(max_length=16, verbose_name='Компонент')),
                ('modelname', models.CharField(max_length=64, verbose_name='Модель')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('log', models.TextField()),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'История Объекта',
                'verbose_name_plural': 'Истории Объектов',
                'ordering': ('componentname', 'modelname', 'date'),
            },
        ),
    ]