# Generated by Django 3.2.13 on 2022-05-14 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_guestemail'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GuestEmail',
        ),
    ]