# Generated by Django 3.0.5 on 2020-05-19 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0010_remove_notification_sendfromid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='sendtoid',
        ),
        migrations.AddField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notify_recipient', to=settings.AUTH_USER_MODEL, verbose_name='Получатель'),
        ),
    ]