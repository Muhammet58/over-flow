# Generated by Django 4.2.3 on 2023-11-28 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_userprofile_last_seen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_seen',
        ),
    ]