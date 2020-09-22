# Generated by Django 3.0.6 on 2020-07-22 18:17

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0029_resume'),
    ]

    operations = [
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=1024, verbose_name='Тема')),
                ('candidatefirstname', models.CharField(max_length=64, verbose_name='Имя')),
                ('candidatemiddlename', models.CharField(max_length=64, verbose_name='Отчество')),
                ('candidatelastname', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('email', models.CharField(blank=True, max_length=64, null=True, verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=16, null=True, verbose_name='Телефон')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание')),
                ('datecreate', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('stafflist', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='summary_stafflist', to='companies.StaffList', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Резюме',
                'verbose_name_plural': 'Резюме',
                'ordering': ('stafflist',),
            },
        ),
        migrations.DeleteModel(
            name='Resume',
        ),
    ]