# Generated by Django 3.2.13 on 2022-05-10 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_coupon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='coupon',
            new_name='code',
        ),
    ]