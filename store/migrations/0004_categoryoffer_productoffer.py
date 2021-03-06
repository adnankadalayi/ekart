# Generated by Django 3.2.13 on 2022-05-07 08:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_remove_category_description'),
        ('store', '0003_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(75)])),
                ('valid_from', models.DateField()),
                ('valid_to', models.DateField()),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='prod_offers', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(75)])),
                ('valid_from', models.DateField()),
                ('valid_to', models.DateField()),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cate_offers', to='category.category')),
            ],
        ),
    ]
