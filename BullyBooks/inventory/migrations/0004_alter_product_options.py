# Generated by Django 5.0.3 on 2024-03-18 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-added_date',)},
        ),
    ]
