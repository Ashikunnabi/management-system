# Generated by Django 3.0.5 on 2020-11-29 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0023_auto_20201127_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='customers',
        ),
    ]
