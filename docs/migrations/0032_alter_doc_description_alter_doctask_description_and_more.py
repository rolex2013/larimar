# Generated by Django 5.0.2 on 2024-02-15 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0031_alter_doctaskcomment_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='doctask',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='docver',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
