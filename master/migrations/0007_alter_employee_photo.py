# Generated by Django 5.0.1 on 2024-06-28 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0006_alter_employee_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
