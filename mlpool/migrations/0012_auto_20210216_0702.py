# Generated by Django 3.1.6 on 2021-02-16 07:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlpool', '0011_auto_20210215_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='time_spent',
        ),
        migrations.AddField(
            model_name='userrequest',
            name='spent_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]