# Generated by Django 3.2.13 on 2022-05-07 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20220507_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryoffer',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='productoffer',
            name='is_active',
        ),
    ]
