# Generated by Django 4.2.3 on 2023-11-28 18:36

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_userprofile_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
