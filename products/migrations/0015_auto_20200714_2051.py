# Generated by Django 3.0.8 on 2020-07-14 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20200714_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]