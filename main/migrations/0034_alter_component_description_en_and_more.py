# Generated by Django 4.1.7 on 2023-12-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_component_is_client_default_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='description_en',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Описание_en'),
        ),
        migrations.AlterField(
            model_name='component',
            name='description_ru',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Описание_ru'),
        ),
        migrations.AlterField(
            model_name='component',
            name='menu_en',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Пункт меню_en'),
        ),
        migrations.AlterField(
            model_name='component',
            name='menu_ru',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Пункт меню_ru'),
        ),
        migrations.AlterField(
            model_name='component',
            name='name_en',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Наименование_en'),
        ),
        migrations.AlterField(
            model_name='component',
            name='name_ru',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Наименование_ru'),
        ),
        migrations.AlterField(
            model_name='dict_protocoltype',
            name='name_en',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Наименование_en'),
        ),
        migrations.AlterField(
            model_name='dict_protocoltype',
            name='name_ru',
            field=models.CharField(max_length=64, verbose_name='Наименование_ru'),
        ),
        migrations.AlterField(
            model_name='dict_theme',
            name='description_en',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Описание_en'),
        ),
        migrations.AlterField(
            model_name='dict_theme',
            name='description_ru',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Описание_ru'),
        ),
        migrations.AlterField(
            model_name='dict_theme',
            name='name_en',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Наименование_en'),
        ),
        migrations.AlterField(
            model_name='dict_theme',
            name='name_ru',
            field=models.CharField(max_length=64, verbose_name='Наименование_ru'),
        ),
        migrations.AlterField(
            model_name='meta_objecttype',
            name='name_en',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Наименование_en'),
        ),
        migrations.AlterField(
            model_name='meta_objecttype',
            name='name_ru',
            field=models.CharField(max_length=64, verbose_name='Наименование_ru'),
        ),
        migrations.AlterField(
            model_name='meta_param',
            name='name_en',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Наименование_en'),
        ),
        migrations.AlterField(
            model_name='meta_param',
            name='name_ru',
            field=models.CharField(max_length=64, verbose_name='Наименование_ru'),
        ),
    ]