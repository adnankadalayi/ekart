# Generated by Django 3.2.13 on 2022-04-26 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_img',
            field=models.ImageField(upload_to='photos/categories'),
        ),
    ]
