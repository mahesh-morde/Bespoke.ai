# Generated by Django 4.2.7 on 2023-11-12 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_catalog'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='catalog',
            table='product_catalog_product_catalog',
        ),
    ]
