# Generated by Django 5.0.3 on 2024-03-28 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_userprofile_is_buyer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='is_buyer',
            new_name='is_seller',
        ),
    ]