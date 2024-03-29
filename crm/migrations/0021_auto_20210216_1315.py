# Generated by Django 3.1.5 on 2021-02-16 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0020_clientevent_place'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='clientstatuslog',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='clientstatuslog',
            name='author',
        ),
        migrations.RemoveField(
            model_name='clientstatuslog',
            name='client',
        ),
        migrations.RemoveField(
            model_name='clientstatuslog',
            name='status',
        ),
        migrations.AlterUniqueTogether(
            name='clienttaskstatuslog',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='clienttaskstatuslog',
            name='author',
        ),
        migrations.RemoveField(
            model_name='clienttaskstatuslog',
            name='status',
        ),
        migrations.RemoveField(
            model_name='clienttaskstatuslog',
            name='task',
        ),
        migrations.RemoveField(
            model_name='clienttask',
            name='typeevent',
        ),
        migrations.DeleteModel(
            name='ClientEventStatusLog',
        ),
        migrations.DeleteModel(
            name='ClientStatusLog',
        ),
        migrations.DeleteModel(
            name='ClientTaskStatusLog',
        ),
    ]
