# Generated by Django 5.0.1 on 2024-06-25 12:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='master.user'),
        ),
    ]
