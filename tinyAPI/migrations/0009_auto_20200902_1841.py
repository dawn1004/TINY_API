# Generated by Django 2.1 on 2020-09-02 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinyAPI', '0008_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
