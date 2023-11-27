# Generated by Django 4.2.3 on 2023-11-22 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0020_tags_question_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='tags',
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='pages.tags'),
        ),
    ]