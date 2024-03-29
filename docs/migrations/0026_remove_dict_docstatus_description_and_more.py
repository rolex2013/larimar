# Generated by Django 4.1.7 on 2024-01-11 10:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("docs", "0025_auto_20210714_1355"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dict_docstatus",
            name="description",
        ),
        migrations.RemoveField(
            model_name="dict_docstatus",
            name="name",
        ),
        migrations.RemoveField(
            model_name="dict_docstatus",
            name="name_lang",
        ),
        migrations.RemoveField(
            model_name="dict_doctaskstatus",
            name="description",
        ),
        migrations.RemoveField(
            model_name="dict_doctaskstatus",
            name="name",
        ),
        migrations.RemoveField(
            model_name="dict_doctaskstatus",
            name="name_lang",
        ),
        migrations.RemoveField(
            model_name="dict_doctasktype",
            name="description",
        ),
        migrations.RemoveField(
            model_name="dict_doctasktype",
            name="name",
        ),
        migrations.RemoveField(
            model_name="dict_doctasktype",
            name="name_lang",
        ),
        migrations.RemoveField(
            model_name="dict_doctype",
            name="description",
        ),
        migrations.RemoveField(
            model_name="dict_doctype",
            name="name",
        ),
        migrations.RemoveField(
            model_name="dict_doctype",
            name="name_lang",
        ),
        migrations.AddField(
            model_name="dict_docstatus",
            name="description_en",
            field=models.TextField(blank=True, null=True, verbose_name="Описание_en"),
        ),
        migrations.AddField(
            model_name="dict_docstatus",
            name="description_ru",
            field=models.TextField(blank=True, null=True, verbose_name="Описание_ru"),
        ),
        migrations.AddField(
            model_name="dict_docstatus",
            name="name_en",
            field=models.CharField(
                default=0, max_length=64, verbose_name="Наименование_en"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dict_docstatus",
            name="name_ru",
            field=models.CharField(
                default=0, max_length=64, verbose_name="Наименование_ru"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dict_doctaskstatus",
            name="description_en",
            field=models.TextField(blank=True, null=True, verbose_name="Описание_en"),
        ),
        migrations.AddField(
            model_name="dict_doctaskstatus",
            name="description_ru",
            field=models.TextField(blank=True, null=True, verbose_name="Описание_ru"),
        ),
        migrations.AddField(
            model_name="dict_doctaskstatus",
            name="name_en",
            field=models.CharField(
                default=0, max_length=64, verbose_name="Наименование_en"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dict_doctaskstatus",
            name="name_ru",
            field=models.CharField(
                default=0, max_length=64, verbose_name="Наименование_ru"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dict_doctasktype",
            name="description_en",
            field=models.TextField(blank=True, null=True, verbose_name="Описание_en"),
        ),
        migrations.AddField(
            model_name="dict_doctasktype",
            name="description_ru",
            field=models.TextField(blank=True, null=True, verbose_name="Описание_ru"),
        ),
        migrations.AddField(
            model_name="dict_doctasktype",
            name="name_en",
            field=models.CharField(
                default=0, max_length=64, verbose_name="Наименование_en"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dict_doctasktype",
            name="name_ru",
            field=models.CharField(
                default=0, max_length=64, verbose_name="Наименование_ru"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dict_doctype",
            name="description_en",
            field=models.TextField(blank=True, null=True, verbose_name="Описание_en"),
        ),
        migrations.AddField(
            model_name="dict_doctype",
            name="description_ru",
            field=models.TextField(blank=True, null=True, verbose_name="Описание_ru"),
        ),
        migrations.AddField(
            model_name="dict_doctype",
            name="name_en",
            field=models.CharField(
                default=0, max_length=64, verbose_name="Наименование_en"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dict_doctype",
            name="name_ru",
            field=models.CharField(
                default=1, max_length=64, verbose_name="Наименование_ru"
            ),
            preserve_default=False,
        ),
    ]
