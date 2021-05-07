# Generated by Django 3.1.5 on 2021-04-28 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doc',
            name='dateclose',
        ),
        migrations.AddField(
            model_name='doc',
            name='manager',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='result_manager_doc', to='auth.user', verbose_name='Менеджер документа'),
            preserve_default=False,
        ),
    ]