# Generated by Django 5.0.3 on 2024-03-28 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_remove_userprofile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_buyer',
            field=models.BooleanField(default=False),
        ),
    ]
