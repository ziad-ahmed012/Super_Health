# Generated by Django 5.0.4 on 2024-05-29 19:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_session_end_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='end_datetime',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 29, 19, 42, 24, 848904, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_datetime',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 29, 19, 42, 24, 848904, tzinfo=datetime.timezone.utc)),
        ),
    ]