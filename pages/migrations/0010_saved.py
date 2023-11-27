# Generated by Django 4.2.3 on 2023-11-21 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0009_alter_answer_answer_alter_question_context'),
    ]

    operations = [
        migrations.CreateModel(
            name='saved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('que', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]