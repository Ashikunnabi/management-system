# Generated by Django 3.0.5 on 2020-04-27 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='feature',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='permission_feature', to='rbac.Feature'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feature',
            name='customers',
            field=models.ManyToManyField(related_name='feature_customers', to='rbac.Customer'),
        ),
        migrations.AlterField(
            model_name='group',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='group_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='user_role', to='rbac.Role'),
        ),
    ]
