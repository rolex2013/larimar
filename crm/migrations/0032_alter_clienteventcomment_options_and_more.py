# Generated by Django 4.1.7 on 2024-01-30 17:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0031_alter_clienteventcomment_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="clienteventcomment",
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.AlterModelOptions(
            name="clienttaskcomment",
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
    ]
