# Generated by Django 4.1.7 on 2024-02-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0039_alter_company_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="content",
            name="datebegin",
            field=models.DateTimeField(verbose_name="Дата публикации"),
        ),
        migrations.AlterField(
            model_name="content",
            name="dateend",
            field=models.DateTimeField(verbose_name="Дата снятия с публикации"),
        ),
    ]
