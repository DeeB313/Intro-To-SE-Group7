# Generated by Django 5.0.3 on 2024-03-28 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_userprofile_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='status',
        ),
    ]
