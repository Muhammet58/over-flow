# Generated by Django 4.2.3 on 2023-11-28 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pics/user-default.png', null=True, upload_to='profile_pics/'),
        ),
    ]
