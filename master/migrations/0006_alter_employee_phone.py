# Generated by Django 5.0.1 on 2024-06-27 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0005_employee_created_by_employee_created_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
