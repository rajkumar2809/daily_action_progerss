# Generated by Django 4.1.1 on 2022-09-27 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_app', '0003_tasks_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='time_taken',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
