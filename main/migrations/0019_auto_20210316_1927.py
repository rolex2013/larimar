# Generated by Django 3.1.5 on 2021-03-16 16:27

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_menu_menuitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='component',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menuitem_component', to='main.component', verbose_name='Компонент'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menuitem_children', to='main.menuitem', verbose_name='Головной пункт меню'),
        ),
    ]
