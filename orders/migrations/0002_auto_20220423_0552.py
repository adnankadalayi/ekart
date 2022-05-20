# Generated by Django 3.2.13 on 2022-04-23 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Ordered', 'Ordered'), ('Shipped', 'Shipped'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Returned', 'Returned'), ('Cancellded', 'Cancelled')], default='Ordered', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product_price',
            field=models.FloatField(null=True),
        ),
    ]