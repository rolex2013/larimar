# Generated by Django 3.1.5 on 2021-07-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0024_auto_20210420_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfile',
            name='psize',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
    ]