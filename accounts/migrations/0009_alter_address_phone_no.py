# Generated by Django 3.2.13 on 2022-05-09 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_address_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone_no',
            field=models.CharField(max_length=10),
        ),
    ]
