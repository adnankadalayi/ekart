# Generated by Django 3.2.13 on 2022-05-10 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_address_phone_no'),
        ('cart', '0005_alter_coupon_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.address'),
        ),
    ]
