# Generated by Django 3.0.5 on 2021-01-24 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0030_auto_20210122_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='path',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]