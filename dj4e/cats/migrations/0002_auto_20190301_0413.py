# Generated by Django 2.1.5 on 2019-03-01 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cat',
            old_name='mileage',
            new_name='weight',
        ),
    ]
