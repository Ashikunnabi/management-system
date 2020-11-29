# Generated by Django 3.0.5 on 2020-11-28 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20201127_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='unit',
        ),
        migrations.AddField(
            model_name='product',
            name='unit_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='product_unit_type', to='inventory.UnitType'),
            preserve_default=False,
        ),
    ]