# Generated by Django 3.0.5 on 2020-07-04 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0012_auto_20200624_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='order_for_sidebar',
            field=models.FloatField(default=1111),
        ),
    ]
