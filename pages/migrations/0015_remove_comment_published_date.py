# Generated by Django 4.2.3 on 2023-11-21 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_comment_published_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='published_date',
        ),
    ]
