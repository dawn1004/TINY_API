# Generated by Django 2.1 on 2020-08-20 10:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinyAPI', '0006_dean_executive_population_random'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='event',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='date_end',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='date_start',
            field=models.DateField(default=datetime.date.today),
        ),
    ]