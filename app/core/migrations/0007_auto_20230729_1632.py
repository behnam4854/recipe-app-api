# Generated by Django 2.1.15 on 2023-07-29 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20230729_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='time_miniutes',
            new_name='time_minutes',
        ),
    ]