# Generated by Django 4.2.3 on 2023-11-21 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_remove_comment_published_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='published_date',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]