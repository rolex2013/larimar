# Generated by Django 3.1.5 on 2021-05-07 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0033_auto_20200724_1449'),
        ('docs', '0016_auto_20210507_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='docver',
            name='company',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, related_name='docver_company', to='companies.company', verbose_name='Организация'),
            preserve_default=False,
        ),
    ]
