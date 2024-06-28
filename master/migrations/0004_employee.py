# Generated by Django 5.0.1 on 2024-06-27 05:49

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_designation_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('join_date', models.DateField(blank=True, null=True)),
                ('emp_no', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('emp_start_date', models.DateField(blank=True, null=True)),
                ('emp_end_date', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='employee_photos/')),
                ('status', models.CharField(max_length=50)),
                ('department', models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emp_dep', to='master.department')),
                ('designation', models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emp_des', to='master.designation')),
                ('location', models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emp_loc', to='master.location')),
            ],
        ),
    ]