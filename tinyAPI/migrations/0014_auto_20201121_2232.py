# Generated by Django 2.1 on 2020-11-21 14:32

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinyAPI', '0013_chatbotsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='campus',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, size=None),
        ),
    ]
