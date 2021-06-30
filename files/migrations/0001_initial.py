# Generated by Django 3.1.5 on 2021-06-30 11:55

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0023_dict_theme'),
        ('companies', '0033_auto_20200724_1449'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dict_FolderType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование')),
                ('sort', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
                ('name_lang', models.CharField(blank=True, max_length=64, null=True, verbose_name='Перевод')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Тип содержимого папки',
                'verbose_name_plural': 'Типы содержимого папок',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Описание')),
                ('datecreate', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('dateclose', models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_company', to='companies.company', verbose_name='Компания')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folder_children', to='files.folder', verbose_name='Проект верхнего уровня')),
                ('theme', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='folder_type', to='main.dict_theme', verbose_name='Тип')),
                ('type', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='folder_type', to='files.dict_foldertype', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Папка',
                'verbose_name_plural': 'Папки',
            },
        ),
        migrations.CreateModel(
            name='FolderFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Наименование')),
                ('uname', models.CharField(blank=True, max_length=255, null=True, verbose_name='Уникальное наименование')),
                ('pfile', models.FileField(blank=True, null=True, upload_to='uploads/files/files', verbose_name='Файл')),
                ('psize', models.CharField(editable=False, max_length=64)),
                ('datecreate', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folder_file', to='files.folder', verbose_name='Папка')),
            ],
            options={
                'verbose_name': 'Файлы',
                'verbose_name_plural': 'Файлы',
            },
        ),
    ]
