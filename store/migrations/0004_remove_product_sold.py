# Generated by Django 5.1.7 on 2025-03-23 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_sold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sold',
        ),
    ]
