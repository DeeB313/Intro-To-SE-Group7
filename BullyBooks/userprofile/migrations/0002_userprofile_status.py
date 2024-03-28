# Generated by Django 5.0.3 on 2024-03-27 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.CharField(choices=[('User', 'User'), ('Admin', 'Admin'), ('Buyer', 'Buyer')], default='User', max_length=50),
        ),
    ]