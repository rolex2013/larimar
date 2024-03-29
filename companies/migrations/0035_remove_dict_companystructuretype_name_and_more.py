# Generated by Django 4.1.7 on 2023-12-07 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0034_company_is_support'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dict_companystructuretype',
            name='name',
        ),
        migrations.RemoveField(
            model_name='dict_companystructuretype',
            name='name_lang',
        ),
        migrations.RemoveField(
            model_name='dict_companytype',
            name='name',
        ),
        migrations.RemoveField(
            model_name='dict_companytype',
            name='name_lang',
        ),
        migrations.RemoveField(
            model_name='dict_contentplace',
            name='name',
        ),
        migrations.RemoveField(
            model_name='dict_contentplace',
            name='name_lang',
        ),
        migrations.RemoveField(
            model_name='dict_contenttype',
            name='name',
        ),
        migrations.RemoveField(
            model_name='dict_contenttype',
            name='name_lang',
        ),
        migrations.RemoveField(
            model_name='dict_positiontype',
            name='name',
        ),
        migrations.RemoveField(
            model_name='dict_positiontype',
            name='name_lang',
        ),
        migrations.AddField(
            model_name='dict_companystructuretype',
            name='name_en',
            field=models.CharField(default='', max_length=64, verbose_name='Наименование_en'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dict_companystructuretype',
            name='name_ru',
            field=models.CharField(default='', max_length=64, verbose_name='Наименование_ru'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dict_companytype',
            name='name_en',
            field=models.CharField(default='', max_length=64, verbose_name='Наименование_en'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dict_companytype',
            name='name_ru',
            field=models.CharField(default='', max_length=64, verbose_name='Наименование_ru'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dict_contentplace',
            name='name_en',
            field=models.CharField(default='', max_length=64, verbose_name='Наименование_en'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dict_contentplace',
            name='name_ru',
            field=models.CharField(default='', max_length=64, verbose_name='Наименование_ru'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dict_contenttype',
            name='name_en',
            field=models.CharField(default='', max_length=64, verbose_name='Наименование_en'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dict_contenttype',
            name='name_ru',
            field=models.CharField(default='', max_length=64, verbose_name='Наименование_ru'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dict_positiontype',
            name='name_en',
            field=models.CharField(default='', max_length=64, verbose_name='Наименование_en'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dict_positiontype',
            name='name_ru',
            field=models.CharField(default='', max_length=64, verbose_name='Наименование_ru'),
            preserve_default=False,
        ),
    ]
