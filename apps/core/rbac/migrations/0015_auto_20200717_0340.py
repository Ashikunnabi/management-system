# Generated by Django 3.0.5 on 2020-07-17 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0014_auto_20200706_1944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='status',
            new_name='is_active',
        ),
    ]
