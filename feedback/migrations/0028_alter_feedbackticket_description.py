# Generated by Django 5.0.2 on 2024-02-15 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0027_alter_feedbacktask_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackticket',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
