# Generated by Django 5.0.6 on 2024-07-01 09:22

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0008_alter_employee_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('VIEWER', 'VIEWER')], max_length=10),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('skill_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('skill_name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='master.employee')),
            ],
        ),
    ]