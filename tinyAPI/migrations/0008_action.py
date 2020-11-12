# Generated by Django 2.1 on 2020-09-02 10:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinyAPI', '0007_auto_20200820_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=150)),
                ('date', models.DateField(default=datetime.date.today)),
                ('time', models.TimeField()),
            ],
        ),
    ]
