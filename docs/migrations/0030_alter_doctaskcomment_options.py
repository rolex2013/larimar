# Generated by Django 4.1.7 on 2024-01-30 17:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("docs", "0029_alter_dict_docstatus_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="doctaskcomment",
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
    ]