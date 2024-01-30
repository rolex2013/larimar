# Generated by Django 4.1.7 on 2024-01-30 17:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("docs", "0028_alter_dict_docstatus_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dict_docstatus",
            options={
                "ordering": ["sort"],
                "verbose_name": "Статус документа",
                "verbose_name_plural": "Статусы документов",
            },
        ),
        migrations.AlterModelOptions(
            name="dict_doctaskstatus",
            options={
                "ordering": ["sort"],
                "verbose_name": "Статус задачи",
                "verbose_name_plural": "Статусы задач",
            },
        ),
        migrations.AlterModelOptions(
            name="dict_doctasktype",
            options={
                "ordering": ["sort"],
                "verbose_name": "Тип задачи",
                "verbose_name_plural": "Типы задач",
            },
        ),
        migrations.AlterModelOptions(
            name="dict_doctype",
            options={
                "ordering": ["sort"],
                "verbose_name": "Тип документа",
                "verbose_name_plural": "Типы документов",
            },
        ),
        migrations.AlterModelOptions(
            name="doctaskcomment",
            options={},
        ),
    ]
