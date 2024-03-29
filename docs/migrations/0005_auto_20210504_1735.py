# Generated by Django 3.1.5 on 2021-05-04 14:35

# import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docs', '0004_auto_20210504_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dict_DocTaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('sort', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
                ('name_lang', models.CharField(blank=True, max_length=64, null=True, verbose_name='Перевод')),
                ('is_close', models.BooleanField(default=False, verbose_name='Закрывает задачу')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Статус задачи',
                'verbose_name_plural': 'Статусы задач',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='Dict_DocTaskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('sort', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
                ('name_lang', models.CharField(blank=True, max_length=64, null=True, verbose_name='Перевод')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Тип задачи',
                'verbose_name_plural': 'Типы задач',
                'ordering': ('sort',),
            },
        ),
        migrations.AlterModelOptions(
            name='docver',
            options={'verbose_name': 'Версия Документа'},
        ),
        migrations.CreateModel(
            name='DocTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('dateend', models.DateField(verbose_name='Окончание')),
                ('datecreate', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('dateclose', models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('assigner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctask_assigner', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultdoctaskuser', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultdoc', to='docs.doc', verbose_name='Документ')),
                ('docver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultdocver', to='docs.docver', verbose_name='Версия Документа')),
                ('status', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='doctask_status', to='docs.dict_doctaskstatus', verbose_name='Статус')),
                ('type', models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctask_type', to='docs.dict_doctasktype', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
    ]
