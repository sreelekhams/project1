# Generated by Django 5.0.6 on 2024-07-01 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0009_alter_user_role_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='skill_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]