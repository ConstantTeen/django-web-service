# Generated by Django 3.1.6 on 2021-02-12 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlpool', '0004_auto_20210212_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlmodel',
            name='binary_body',
            field=models.FileField(upload_to='uploads'),
        ),
    ]