# Generated by Django 3.0.5 on 2020-05-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0007_auto_20200522_0911'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(blank=True, max_length=500)),
                ('updated_by', models.CharField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('store_json', models.TextField(blank=True)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
