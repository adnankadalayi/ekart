# Generated by Django 3.2.13 on 2022-05-15 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoffer',
            name='valid_from',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='categoryoffer',
            name='valid_to',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='valid_from',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='valid_to',
            field=models.DateTimeField(),
        ),
    ]
