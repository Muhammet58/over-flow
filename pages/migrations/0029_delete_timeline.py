# Generated by Django 4.2.3 on 2023-12-05 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0028_remove_timeline_answer_remove_timeline_comment_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='timeline',
        ),
    ]