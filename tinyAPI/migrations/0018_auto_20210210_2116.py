# Generated by Django 2.1 on 2021-02-10 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinyAPI', '0017_betatest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='betatest',
            name='accuracy',
            field=models.DecimalField(decimal_places=2, max_digits=2),
        ),
    ]
