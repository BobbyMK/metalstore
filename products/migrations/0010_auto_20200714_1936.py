# Generated by Django 3.0.8 on 2020-07-14 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20200714_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='static/img/products_images/'),
        ),
    ]
