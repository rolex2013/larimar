# Generated by Django 4.1.7 on 2023-11-22 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.utils_lang


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0034_company_is_support'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dict_YListFieldType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ru', models.CharField(max_length=128, verbose_name='Наименование_ru')),
                ('name_en', models.CharField(max_length=128, verbose_name='Наименование_en')),
                ('description_ru', models.TextField(blank=True, null=True, verbose_name='Описание_ru')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Описание_en')),
                ('sort', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Сортировка')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Тип данных',
                'verbose_name_plural': 'Типы данных',
                'ordering': ('sort',),
            },
            bases=(main.utils_lang.TranslateFieldMixin, models.Model),
        ),
        migrations.CreateModel(
            name='YList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('fieldslist', models.CharField(max_length=1024, verbose_name='Список и тип полей')),
                ('datecreate', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('dateupdate', models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')),
                ('dateclose', models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность Списка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ylist_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('authorupdate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ylist_author_update', to=settings.AUTH_USER_MODEL, verbose_name='Автор последних изменений')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ylistresultcompany', to='companies.company', verbose_name='Компания')),
                ('members', models.ManyToManyField(related_name='ylist_members', to=settings.AUTH_USER_MODEL, verbose_name='Участники')),
            ],
            options={
                'verbose_name': 'Список',
                'verbose_name_plural': 'Списки',
            },
        ),
        migrations.CreateModel(
            name='YListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fieldslist', models.TextField(blank=True, null=True, verbose_name='Список и значения полей')),
                ('sort', models.PositiveSmallIntegerField(blank=True, default=5, null=True)),
                ('datecreate', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('dateupdate', models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')),
                ('dateclose', models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность элемента Списка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ylistitem_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('authorupdate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ylistitem_author_update', to=settings.AUTH_USER_MODEL, verbose_name='Автор последних изменений')),
                ('ylist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ylistresult', to='lists.ylist', verbose_name='Список')),
            ],
            options={
                'verbose_name': 'Запись списка',
                'verbose_name_plural': 'Записи списков',
                'ordering': ('sort',),
            },
        ),
    ]
