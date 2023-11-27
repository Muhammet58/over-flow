# Generated by Django 4.2.3 on 2023-11-21 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_saved'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('comment_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.answer')),
            ],
        ),
    ]
