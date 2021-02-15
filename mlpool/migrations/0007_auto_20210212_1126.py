# Generated by Django 3.1.6 on 2021-02-12 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mlpool', '0006_userrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrequest',
            name='input_data',
        ),
        migrations.RemoveField(
            model_name='userrequest',
            name='spent_time',
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('spent_time', models.TimeField(default=0)),
                ('input_data', models.CharField(max_length=4000)),
                ('prediction', models.CharField(max_length=4000)),
                ('ml_model', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mlpool.mlmodel')),
                ('user_request', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mlpool.userrequest')),
            ],
        ),
    ]
